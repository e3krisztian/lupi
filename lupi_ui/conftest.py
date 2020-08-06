from http import HTTPStatus
import flask
from .app import create_app
from . import app
import lupi_game_client

import pytest

@pytest.fixture
def flask_app():
    return create_app(testing=True)


@pytest.fixture
def url_for(flask_app):
    def url_for(*args, **kwargs):
        with flask_app.test_request_context():
            return flask.url_for(*args, **kwargs)
    return url_for


@pytest.fixture
def client(flask_app):
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def game_api() -> lupi_game_client.GameApi:
    with app.game_api() as api:
        yield api


@pytest.fixture
def stats_api() -> lupi_game_client.StatsApi:
    with app.stats_api() as api:
        yield api


@pytest.fixture
def no_active_round(game_api):
    """ Ensure, that the test using this fixture has no active round.
    """
    try:
        round_id = game_api.get_current_round_id()
    except lupi_game_client.ApiException as e:
        assert e.status == HTTPStatus.NOT_FOUND
    else:
        game_api.set_round_completed(round_id, body=True)


@pytest.fixture
def active_round_id(game_api, no_active_round):
    """ Ensure, that the test starts with an empty active round.
    """
    return game_api.create_round()
