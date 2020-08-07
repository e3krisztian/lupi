from functools import partial
from http import HTTPStatus
import os

import flask
from flask import redirect, url_for, flash, request, abort
from flask.templating import render_template
from flask_wtf import FlaskForm
import flask_table
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from . import game_server

flash_info = partial(flash, category='info')
flash_error = partial(flash, category='error')

ui = flask.Blueprint('lupi_ui', __name__)

def render_main_page(vote_form):
    return render_template('main_page.html', form=vote_form)


@ui.route('/')
def index():
    return render_main_page(VoteForm())


class VoteForm(FlaskForm):
    name = StringField(
        label='Name:',
        validators=[DataRequired()])
    number = IntegerField(
        label='Vote (positive integer):',
        validators=[DataRequired(), NumberRange(min=1)])


@ui.route('/vote', methods=['GET', 'POST'])
def vote():
    form = VoteForm()
    if not form.validate_on_submit():
        return render_template('main_page.html', form=form)

    with game_server.open() as server:
        try:
            round_id = server.game.get_current_round_id()
        except game_server.ApiException as e:
            if e.status == HTTPStatus.NOT_FOUND:
                flash_error(f'Can not register vote - there is no active round')
                return render_main_page(form)
        else:
            try:
                vote = game_server.Vote(
                    round_id=round_id,
                    name=form.name.data,
                    number=form.number.data)
                server.game.add_vote(vote)
                flash_info(f'Vote registered in round {round_id}!')
            except game_server.ApiException as e:
                if e.status == HTTPStatus.NOT_FOUND:
                    flash_error(f'Can not register vote - there is no active round')
                elif e.status == HTTPStatus.CONFLICT:
                    flash_error(f'Can not register vote - already voted in round {round_id}')
                return render_main_page(form)

    return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


@ui.route('/start_round', methods=['POST'])
def start_round():
    with game_server.open() as server:
        try:
            round_id = server.game.create_round()
            flash_info(f'New round started: {round_id}')
        except game_server.ApiException:
            flash_error(f'There is already an active round')
        return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


@ui.route('/close_round', methods=['POST'])
def close_round():
    with game_server.open() as server:
        try:
            round_id = server.game.get_current_round_id()
            server.game.set_round_completed(round_id, body=True)
            flash_info(f'Completed round: {round_id}')
        except game_server.ApiException:
            flash_error(f'There is no active round')
        return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


class HistoryTable(flask_table.Table):
    id = flask_table.LinkCol(
        "Round ID",
        "lupi_ui.round_details",
        attr_list=['id'],
        url_kwargs=dict(round_id='id')
    )
    start_date = flask_table.Col("Start date")
    end_date = flask_table.Col("End date")
    players = flask_table.Col("# players")


@ui.route('/history')
def rounds_history():
    page_size = int(request.args.get('page_size', "25"))
    with game_server.open() as server:
        try:
            before = int(request.args['before'])
            if before < 1:
                raise ValueError
            paged_rounds = server.stats.get_rounds(
                before=before,
                page_size=page_size
            )
        except (KeyError, ValueError):
            paged_rounds = server.stats.get_rounds(page_size=page_size)

    if paged_rounds.previous:
        previous = url_for(
            "lupi_ui.rounds_history",
            **paged_rounds.previous.to_dict()
        )
    else:
        previous = None

    return render_template(
        'history.html',
        history_table=HistoryTable(paged_rounds.data, table_id="history"),
        previous=previous)


@ui.route('/rounds/<int:round_id>')
def round_details(round_id):
    with game_server.open() as server:
        try:
            round_details = server.game.get_round(round_id)
        except game_server.ApiException as e:
            flash(f"Round {round_id} is not available: {e}", category="error")
            abort(HTTPStatus.NOT_FOUND)
    return render_template("round_details.html", round_details=round_details)


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(ui)
    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY'].encode()
    try:
        # disable CSRF validation for tests
        app.config['WTF_CSRF_ENABLED'] = os.environ['WTF_CSRF_ENABLED'].lower() not in ['false', '0', 'off']
    except KeyError:
        pass
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='5000')
