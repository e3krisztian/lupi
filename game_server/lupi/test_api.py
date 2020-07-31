# test endpoints via openapi.yaml

from http import HTTPStatus
import pytest

from .model import db, Round, Vote
from . import data as game


class Test_v1_rounds:
    URL = '/v1/rounds'

    def test_get(self, client):
        rv = client.get(self.URL)
        assert rv.status_code == HTTPStatus.OK
        assert rv.json == [1, 2]

    def test_post_creates_current_round(self, client):
        rv = client.post(self.URL)

        assert rv.status_code == HTTPStatus.CREATED

        round_id = rv.json
        assert isinstance(round_id, int)

        round = db.session.query(Round).get(round_id)
        assert round

    def test_post_existing_round_returns_conflict(self, client):
        game.make_round()
        rv = client.post(self.URL)
        assert rv.status_code == HTTPStatus.CONFLICT


def test_post_v1_votes(client):
    rv = client.post('/v1/votes', json=dict(round="2", user='voter', vote=2))
    assert rv.status_code == HTTPStatus.OK


@pytest.fixture
def round_id_1(db):
    """ Create an active round with id 1 """
    round = game.make_round()
    round.id = 1
    db.session.flush()
    return 1


class Test_v1_rounds_roundid_is_completed:
    """ This endpoint closes a round """

    def url(self, round_id):
        return f'/v1/rounds/{round_id}/is_completed'

    @pytest.mark.parametrize("round_id", ["current", "1"])
    def test_put_True_completes_round(self, client, round_id, round_id_1):
        assert game.get_current_round_id() == 1

        rv = client.put(self.url(round_id), json=True)
        assert rv.status_code == HTTPStatus.NO_CONTENT

        with pytest.raises(LookupError):
            game.get_current_round_id()

    @pytest.mark.parametrize("round_id", ["current", "1"])
    def test_put_False_succeeds_on_active_round(self, client, round_id, round_id_1):
        rv = client.put(self.url(round_id), json=False)

        assert rv.status_code == HTTPStatus.NO_CONTENT
        assert game.get_current_round_id() == 1

    def test_put_False_fails_on_completed_round(self, client, round_id_1):
        game.complete_round()

        rv = client.put(self.url(round_id_1), json=False)

        assert rv.status_code == HTTPStatus.CONFLICT

    def test_put_True_on_non_active_round(self, client, round_id_1):
        game.complete_round()

        rv = client.put(self.url(round_id_1), json=True)

        assert rv.status_code == HTTPStatus.NO_CONTENT

    def test_put_with_current_when_no_active_round(self, client):
        rv = client.put(self.url("current"), json=True)

        assert rv.status_code == HTTPStatus.NOT_FOUND



def test_get_v1_rounds_current_id(client):
    rv = client.get('/v1/rounds/current/id')
    assert rv.status_code == HTTPStatus.OK


def test_get_v1_rounds_current_result(client):
    rv = client.get('/v1/rounds/current/result')
    assert rv.status_code == HTTPStatus.OK


def test_get_v1_rounds_1_result(client):
    rv = client.get('/v1/rounds/1/result')
    assert rv.status_code == HTTPStatus.OK


def test_get_v1_rounds_current(client):
    rv = client.get('/v1/rounds/current')
    assert rv.status_code == HTTPStatus.OK


def test_get_v1_rounds_1(client):
    rv = client.get('/v1/rounds/1')
    assert rv.status_code == HTTPStatus.OK
