# see openapi.yaml for detailed endpoint definitions

from http import HTTPStatus

from flask import request
import flask
from . import game
from . import stats


def get_rounds(before=None, limit=25):
    """ GET /v1/rounds?before=id&limit=max-items """
    rounds = stats.get_rounds(before, limit)
    output = {
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
    if len(rounds) == limit:
        output['previous'] = f"/v1/rounds?before={rounds[-1].id}&limit={limit}"
    return output, HTTPStatus.OK


def create_round():
    """ POST /v1/rounds """
    try:
        round = game.make_round()
        return round.id, HTTPStatus.CREATED, {'Location': f'/v1/rounds/{round.id}'}
    except game.Error:
        return None, HTTPStatus.CONFLICT


def add_vote():
    """ POST /v1/votes """
    round = game.get_round(request.json['round'])
    name = request.json['name']
    number = request.json['number']
    game.add_vote(round, name, number)
    return None, HTTPStatus.OK


def complete_round(round):
    """ PUT /v1/rounds/{round}/is_completed """
    requested_round = game.get_round(round)
    if requested_round is None:
        return None, HTTPStatus.NOT_FOUND
    do_complete = request.json

    if requested_round.is_completed and not do_complete:
        return None, HTTPStatus.CONFLICT
    if do_complete and not requested_round.is_completed:
        game.complete_round(requested_round)


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
        id=1,
        start_date='2020-07-30T17:40:40.123123Z',
        end_date='2020-07-30T17:45:40.123123Z',
        is_completed=True,
        players=8,
    )
