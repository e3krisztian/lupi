from http import HTTPStatus
import flask
from flask.testing import FlaskClient
from .app import create_app
from . import game_server

import pytest

class WebUI:
    def __init__(self):
        self.app = create_app(testing=True)

    def url_for(self, *args, **kwargs):
        with self.app.test_request_context():
            return flask.url_for(*args, **kwargs)


@pytest.fixture
def webui() -> WebUI:
    return WebUI()


@pytest.fixture
def server() -> game_server.ServerApi:
    with game_server.open() as server:
        yield server


@pytest.fixture
def client(webui) -> FlaskClient:
    with webui.app.test_client() as client:
        yield client


@pytest.fixture
def no_active_round(server):
    """ Ensure, that the test using this fixture has no active round.
    """
    try:
        round_id = server.game.get_current_round_id()
    except game_server.ApiException as e:
        assert e.status == HTTPStatus.NOT_FOUND
    else:
        server.game.set_round_completed(round_id, body=True)


@pytest.fixture
def active_round_id(server, no_active_round):
    """ Ensure, that the test starts with an empty active round.
    """
    return server.game.create_round()
