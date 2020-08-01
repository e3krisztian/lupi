"""
Current game.

Caveat: this implementation potentially leads to data anomalies
due to concurrent usage.

Should have used redis and conditional redis transactions instead as data store
(redis processes requests in a single thread, serialized).
"""

from datetime import datetime

import sqlalchemy
from .model import db, Round, Vote


RoundId = int


class Error(Exception):
    pass


def get_round(round_id: str) -> Round:
    if round_id == "current":
        round = _get_current_round()
    else:
        round = db.session.query(Round).get(RoundId(round_id))
    return round


def get_current_round_id() -> RoundId:
    round = _get_current_round()
    if round is None:
        raise LookupError("No current round")
    return round.id


def make_round() -> Round:
    if _query_active_rounds().first() is not None:
        raise Error("Active round exists")

    round = Round(start_date=datetime.utcnow())
    db.session.add(round)
    db.session.flush()
    return round


def complete_round(round):
    if round != _get_current_round():
        raise Error('round is not the currently active one')
    if round is not None:
        round.end_date = datetime.utcnow()

    # close other open rounds
    for round in _query_active_rounds():
        round.end_date = round.start_date


def add_vote(round, name, number):
    if round != _get_current_round():
        raise Error('round is not the currently active one')
    if round is None:
        raise Error("No current round")
    round.votes.append(Vote(name=name, number=number))
    try:
        db.session.flush()
    except sqlalchemy.exc.IntegrityError as e:
        raise Error from e


#
def _query_active_rounds():
    return db.session.query(Round).filter_by(end_date=None)


def _get_current_round() -> Round:
    return (
        _query_active_rounds()
        .order_by(Round.id.asc())
        .first()
    )
