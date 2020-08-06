import contextlib
from http import HTTPStatus
import os

import flask
from flask import redirect, url_for, flash
from flask.templating import render_template

import lupi_game_client


ui = flask.Blueprint('lupi_ui', __name__)


v1_configuration = lupi_game_client.Configuration(
    host = "http://game_server:8080/v1"
)


@contextlib.contextmanager
def game_api() -> lupi_game_client.GameApi:
    with lupi_game_client.ApiClient(v1_configuration) as api_client:
        yield lupi_game_client.GameApi(api_client)


@contextlib.contextmanager
def stats_api() -> lupi_game_client.StatsApi:
    with lupi_game_client.ApiClient(v1_configuration) as api_client:
        yield lupi_game_client.StatsApi(api_client)


@ui.route('/')
def index():
    return render_template('main_page.html')


@ui.route('/start_round', methods=['POST'])
def start_round():
    with game_api() as api:
        try:
            round_id = api.create_round()
            flash(f'New round started: {round_id}')
        except lupi_game_client.ApiException:
            flash(f'There is already an active round, close it before starting a new one', category='error')
        return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


@ui.route('/close_round', methods=['POST'])
def close_round():
    with game_api() as api:
        try:
            round_id = api.get_current_round_id()
            api.set_round_completed(round_id, body=True)
            flash(f'Completed round: {round_id}')
        except lupi_game_client.ApiException:
            flash(f'There was no active round to complete')
        return redirect(url_for('lupi_ui.index'), HTTPStatus.SEE_OTHER)


def create_app(testing=False):
    app = flask.Flask(__name__)
    app.register_blueprint(ui)
    app.config['TESTING'] = testing
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY'].encode()
    return app


if __name__ == '__main__':
    app = create_app(testing=True)
    app.run(host='0.0.0.0', port='5000', debug=True)
