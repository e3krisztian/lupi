from http import HTTPStatus
import os

import flask
from flask import redirect, url_for, flash
from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from . import game_server

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
                flash(f'Can not register vote - there is no active round', category='error')
                return render_main_page(form)
        else:
            try:
                vote = game_server.Vote(
                    round_id=round_id,
                    name=form.name.data,
                    number=form.number.data)
                server.game.add_vote(vote)
                flash(f'Thank you for your vote in round {round_id}!')
            except game_server.ApiException as e:
                if e.status == HTTPStatus.NOT_FOUND:
                    flash(f'Can not register vote - there is no active round', category='error')
                elif e.status == HTTPStatus.CONFLICT:
                    flash(f'Can not register vote - already voted in round {round_id}', category='error')
                return render_main_page(form)

    return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


@ui.route('/start_round', methods=['POST'])
def start_round():
    with game_server.open() as server:
        try:
            round_id = server.game.create_round()
            flash(f'New round started: {round_id}')
        except game_server.ApiException:
            flash(f'There is already an active round', category='error')
        return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


@ui.route('/close_round', methods=['POST'])
def close_round():
    with game_server.open() as server:
        try:
            round_id = server.game.get_current_round_id()
            server.game.set_round_completed(round_id, body=True)
            flash(f'Completed round: {round_id}')
        except game_server.ApiException:
            flash(f'There is no active round')
        return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


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
