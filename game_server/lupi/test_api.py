# test endpoints via openapi.yaml

from http import HTTPStatus


def test_get_v1_rounds(client):
    rv = client.get('/v1/rounds')
    assert rv.status_code == HTTPStatus.OK
    assert rv.json == [1, 2]


def test_post_v1_rounds(client):
    rv = client.post('/v1/rounds')
    assert rv.status_code == HTTPStatus.CREATED
    assert rv.json == 1


def test_post_v1_votes(client):
    rv = client.post('/v1/votes', json=dict(round="2", user='voter', vote=2))
    assert rv.status_code == HTTPStatus.OK


def test_put_v1_rounds_current_is_completed(client):
    rv = client.put('/v1/rounds/current/is_completed', json=True)
    assert rv.status_code == HTTPStatus.NO_CONTENT


def test_put_v1_rounds_1_is_completed(client):
    rv = client.put('/v1/rounds/1/is_completed', json=True)
    assert rv.status_code == HTTPStatus.NO_CONTENT


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
