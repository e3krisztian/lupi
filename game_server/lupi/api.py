# see openapi.yaml for detailed endpoint definitions

from http import HTTPStatus

from flask import request, url_for


def get_rounds():
    """ GET /v1/rounds """
    return [1, 2]


def create_round():
    """ POST /v1/rounds """
    round_id = 1
    return round_id, HTTPStatus.CREATED, {'Location': f'/v1/rounds/{round_id}'}


def add_vote():
    """ POST /v1/votes """
    assert 'user' in request.json
    assert 'vote' in request.json
    assert 'round' in request.json
    return None, HTTPStatus.OK


def set_round_is_completed(round):
    """ PUT /v1/rounds/{round}/is_completed """
    print(repr(round))


def get_current_round_id():
    """ GET /v1/rounds/current/id """
    return 1


def get_round_result(round):
    """ GET /v1/rounds/{round}/result """
    print(repr(round))
    return dict(
        is_completed=True,
        winner='winning-user',
        vote=1,
    )


def get_round(round):
    """ GET /v1/rounds/{round} """
    print(repr(round))
    return dict(
        start_date='2020-07-30T17:40:40.123123Z',
        end_date='2020-07-30T17:45:40.123123Z',
        is_completed=True,
        players=8,
    )
