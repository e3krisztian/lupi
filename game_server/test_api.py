# test endpoints via openapi.yaml

from datetime import date, datetime, timedelta, timezone
from http import HTTPStatus

from dateutil.parser import isoparse
import pytest

from .model import db, Round, Vote
from . import game


EPOCH = datetime(1970, 1, 1, 0, 1, 2, 3, tzinfo=timezone.utc)


def _start_date(n):
    return EPOCH + timedelta(hours=2 * n)


def _end_date(n):
    return EPOCH + timedelta(hours=2 * n + 1)


def _make_completed_round(n, votes=()):
    round = Round(start_date=_start_date(n), end_date=_end_date(n))
    round.votes = [Vote(name=name, number=number) for name, number in votes]
    db.session.add(round)
    db.session.commit()
    assert round.is_completed
    return round


class Test_get_v1_rounds:
    URL = '/v1/rounds'

    def test_no_rounds(self, client):
        rv = client.get(self.URL)
        assert rv.status_code == HTTPStatus.OK
        assert rv.json == {'data': []}

    def test_result_is_desc_by_time(self, client):
        # FIXME: this should be a unit test for stats.get_rounds
        r1 = _make_completed_round(1)
        r2 = _make_completed_round(2)
        r3 = _make_completed_round(3)

        rv = client.get(self.URL)
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == [r3.id, r2.id, r1.id]

    def test_not_completed_round_not_listed(self, client):
        # FIXME: this should be a unit test for stats.get_rounds
        r1 = _make_completed_round(1)
        game.make_round()

        rv = client.get(self.URL)

        assert rv.status_code == HTTPStatus.OK
        assert len(rv.json['data']) == 1
        assert rv.json['data'][0]['id'] == r1.id

    def test_data(self, client):
        r1 = _make_completed_round(1, [('a', 1), ('b', 2)])
        r2 = _make_completed_round(2)

        rv = client.get(self.URL)

        assert rv.status_code == HTTPStatus.OK
        data = rv.json
        assert len(data['data']) == 2

        rr0 = data['data'][0]
        assert rr0['id'] == r2.id
        assert datetime_eq(rr0['start_date'], _start_date(2))
        assert datetime_eq(rr0['end_date'], _end_date(2))
        assert rr0['players'] == 0

        rr1 = data['data'][1]
        assert rr1['id'] == r1.id
        assert datetime_eq(rr1['start_date'], _start_date(1))
        assert datetime_eq(rr1['end_date'], _end_date(1))
        assert rr1['players'] == 2  # [('a', 1), ('b', 2)]

    def test_paging_before(self, client):
        r1 = _make_completed_round(1)
        r2 = _make_completed_round(2)
        r3 = _make_completed_round(3)

        rv = client.get(self.URL, query_string={'before': r3.id + 1})
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == [r3.id, r2.id, r1.id]

        rv = client.get(self.URL, query_string={'before': r3.id})
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == [r2.id, r1.id]

        rv = client.get(self.URL, query_string={'before': r2.id})
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == [r1.id]

        rv = client.get(self.URL, query_string={'before': r1.id})
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == []

    def test_paging_limit(self, client):
        r1 = _make_completed_round(1)
        r2 = _make_completed_round(2)
        r3 = _make_completed_round(3)

        rv = client.get(self.URL, query_string={'limit': 2})
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == [r3.id, r2.id]

    def test_paging_previous(self, client):
        r1 = _make_completed_round(1)
        r2 = _make_completed_round(2)
        r3 = _make_completed_round(3)

        rv = client.get(self.URL, query_string={'limit': 1})
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == [r3.id]

        rv = client.get(rv.json['previous'])
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == [r2.id]

        rv = client.get(rv.json['previous'])
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == [r1.id]

        rv = client.get(rv.json['previous'])
        assert rv.status_code == HTTPStatus.OK
        assert [r['id'] for r in rv.json['data']] == []
        assert 'previous' not in rv.json


class Test_post_v1_rounds:
    URL = '/v1/rounds'

    def test_creates_current_round(self, client):
        rv = client.post(self.URL)

        assert rv.status_code == HTTPStatus.CREATED

        round_id = rv.json
        assert isinstance(round_id, int)

        round = db.session.query(Round).get(round_id)
        assert round

    def test_existing_round_returns_conflict(self, client):
        game.make_round()
        rv = client.post(self.URL)
        assert rv.status_code == HTTPStatus.CONFLICT


class Test_post_v1_votes:
    URL = '/v1/votes'

    def test_creates_vote(self, client):
        round = game.make_round()
        vote = dict(round=str(round.id), name='voter', number=2)

        rv = client.post(self.URL, json=vote)

        assert rv.status_code == HTTPStatus.OK
        assert len(round.votes) == 1
        assert round.votes[0].name == 'voter'
        assert round.votes[0].number == 2

    def test_voting_on_nonexisting_round(self, client):
        vote = dict(round="1", name='voter', number=2)
        rv = client.post(self.URL, json=vote)
        assert rv.status_code == HTTPStatus.NOT_FOUND

    def test_voting_on_completed_round(self, client):
        round = _make_completed_round(1)

        vote = dict(round=f"{round.id}", name='voter', number=2)
        rv = client.post(self.URL, json=vote)
        assert rv.status_code == HTTPStatus.CONFLICT

    def test_duplicate_vote(self, client):
        round = game.make_round()
        vote = dict(round=str(round.id), name='voter', number=2)

        rv = client.post(self.URL, json=vote)
        assert rv.status_code == HTTPStatus.OK

        rv = client.post(self.URL, json=vote)
        assert rv.status_code == HTTPStatus.CONFLICT


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
        game.complete_round(game.get_round(round_id_1))

        rv = client.put(self.url(round_id_1), json=False)

        assert rv.status_code == HTTPStatus.CONFLICT

    def test_put_True_on_non_active_round(self, client, round_id_1):
        game.complete_round(game.get_round(round_id_1))

        rv = client.put(self.url(round_id_1), json=True)

        assert rv.status_code == HTTPStatus.NO_CONTENT

    def test_put_with_current_when_no_active_round(self, client):
        rv = client.put(self.url("current"), json=True)

        assert rv.status_code == HTTPStatus.NOT_FOUND


class Test_get_v1_rounds_current_id:

    def test_happy_path(self, client):
        round = game.make_round()

        rv = client.get('/v1/rounds/current/id')

        assert rv.status_code == HTTPStatus.OK
        assert rv.json == round.id

    def test_no_current_round(self, client):
        rv = client.get('/v1/rounds/current/id')

        assert rv.status_code == HTTPStatus.NOT_FOUND


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


def datetime_eq(datetime1, datetime2):
    def _as_datetime(datetimeish):
        assert isinstance(datetimeish, (datetime, str))
        if isinstance(datetimeish, str):
            return isoparse(datetimeish)
        return datetimeish
    return _as_datetime(datetime1) == _as_datetime(datetime2)
