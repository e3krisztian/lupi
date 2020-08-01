"""
Statistics and other info about past games.
"""

from datetime import datetime
from typing import List

from sqlalchemy.orm.query import Query
from .model import db, Round, Vote


RoundId = int


class Error(Exception):
    pass


def get_rounds(before=None, limit=10) -> List[Round]:
    q: Query = (
        db.session.query(Round)
        .filter(Round.end_date != None)
        .order_by(Round.id.desc())
    )

    if before is not None:
        q = q.filter(Round.id < before)

    q = q.limit(limit)

    return q.all()
