from http import HTTPStatus
import os

import flask
from flask import redirect, url_for, flash
from flask.templating import render_template

from . import game_server


ui = flask.Blueprint('lupi_ui', __name__)


@ui.route('/')
def index():
    return render_template('main_page.html')


@ui.route('/start_round', methods=['POST'])
def start_round():
    with game_server.open() as server:
        try:
            round_id = server.game.create_round()
            flash(f'New round started: {round_id}')
        except game_server.ApiException:
            flash(f'There is already an active round, close it before starting a new one', category='error')
        return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


@ui.route('/close_round', methods=['POST'])
def close_round():
    with game_server.open() as server:
        try:
            round_id = server.game.get_current_round_id()
            server.game.set_round_completed(round_id, body=True)
            flash(f'Completed round: {round_id}')
        except game_server.ApiException:
            flash(f'There was no active round to complete')
        return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(ui)
    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY'].encode()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='5000')
