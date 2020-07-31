# see openapi.yaml for detailed endpoint definitions

from http import HTTPStatus

from flask import request
import flask
from . import game


def get_rounds():
    """ GET /v1/rounds """
    # TODO: GET /v1/rounds
    return [1, 2]


def create_round():
    """ POST /v1/rounds """
    try:
        round = game.make_round()
        return round.id, HTTPStatus.CREATED, {'Location': f'/v1/rounds/{round.id}'}
    except game.Error:
        return None, HTTPStatus.CONFLICT


def add_vote():
    """ POST /v1/votes """
    assert 'user' in request.json
    assert 'vote' in request.json
    assert 'round' in request.json
    return None, HTTPStatus.OK


def set_round_is_completed(round):
    """ PUT /v1/rounds/{round}/is_completed """
    requested_round = game.get_round(round)
    if requested_round is None:
        return None, HTTPStatus.NOT_FOUND
    do_complete = request.json

    if requested_round.is_completed and not do_complete:
        return None, HTTPStatus.CONFLICT
    if do_complete and not requested_round.is_completed:
        # according to game rules, there can be only one
        # active round, however the current implementation
        # potentially allows for multiple active rounds (race condition)
        # this is ignored at this point (server error due to assertion).
        assert requested_round.id == game.get_current_round_id()

        game.complete_round()


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
