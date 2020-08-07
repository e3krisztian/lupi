# see openapi.yaml for detailed endpoint definitions

from http import HTTPStatus

from flask import request
import flask
from . import game
from . import stats


# game API
def create_round():
    """ POST /v1/rounds """
    try:
        round = game.make_round()
        return round.id, HTTPStatus.CREATED, {'Location': f'/v1/rounds/{round.id}'}
    except game.Error:
        return None, HTTPStatus.CONFLICT


def add_vote():
    """ POST /v1/votes """
    round = game.get_round(request.json['round_id'])
    if round is None:
        return None, HTTPStatus.NOT_FOUND
    name = request.json['name']
    number = request.json['number']
    try:
        game.add_vote(round, name, number)
        return None, HTTPStatus.OK
    except game.Error:
        return None, HTTPStatus.CONFLICT


def set_round_completed(round_id):
    """ PUT /v1/rounds/{round_id}/is_completed """
    requested_round = game.get_round(round_id)
    if requested_round is None:
        return None, HTTPStatus.NOT_FOUND
    do_complete = request.json

    if requested_round.is_completed and not do_complete:
        return None, HTTPStatus.CONFLICT
    if do_complete and not requested_round.is_completed:
        game.complete_round(requested_round)


def get_current_round_id():
    """ GET /v1/rounds/current/id """
    try:
        return game.get_current_round_id()
    except LookupError:
        return None, HTTPStatus.NOT_FOUND


# stats API
def get_round_result(round_id):
    """ GET /v1/rounds/{round_id}/result """
    # TODO: GET /v1/rounds/{round_id}/result
    print(repr(round))
    return dict(
        is_completed=True,
        winner='winning-user',
        vote=1,
    )


def get_round(round_id):
    """ GET /v1/rounds/{round_id} """
    # TODO: GET /v1/rounds/{round_id}
    print(repr(round))
    return dict(
        id=1,
        start_date='2020-07-30T17:40:40.123123Z',
        end_date='2020-07-30T17:45:40.123123Z',
        is_completed=True,
        players=8,
    )


def get_rounds(before=None, page_size=25):
    """ GET /v1/rounds?before=id&page_size=max-items """
    rounds = stats.get_rounds(before, page_size)
    result = {
        'data': [
            dict(
                id=round.id,
                start_date=round.start_date,
                end_date=round.end_date,
                players=len(round.votes)
            )
            for round in rounds
        ]
    }
    if len(rounds) == page_size:
        result['previous'] = dict(
            before=rounds[-1].id,
            page_size=page_size
        )
    return result, HTTPStatus.OK
