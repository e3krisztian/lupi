"""
Game data.

Caveat: this implementation potentially leads to data anomalies
due to concurrent usage.

Should have used redis and conditional redis transactions instead as data store
(redis processes requests in a single thread, serialized).
"""

from datetime import datetime

import sqlalchemy
from .model import db, Round, Vote


RoundId = int


class GameData:
    class Error(Exception):
        pass

    def get_current_round_id(self) -> RoundId:
        round = self._get_current_round()
        if round is None:
            raise LookupError("No current round")
        return round.id

    def make_round(self) -> Round:
        if self._query_active_rounds().first() is not None:
            raise self.Error("Active round exists")

        round = Round(start_date=datetime.utcnow())
        db.session.add(round)
        db.session.flush()
        return round

    def complete_round(self):
        round = self._get_current_round()
        if round is not None:
            round.end_date = datetime.utcnow()

        # close other open rounds
        for round in self._query_active_rounds():
            round.end_date = round.start_date

    def add_vote(self, name, number):
        round = self._get_current_round()
        if round is None:
            raise self.Error("No current round")
        round.votes.append(Vote(name=name, number=number))
        try:
            db.session.flush()
        except sqlalchemy.exc.IntegrityError as e:
            raise self.Error from e

    #
    def _query_active_rounds(self):
        return db.session.query(Round).filter_by(end_date=None)

    def _get_current_round(self) -> Round:
        return (
            self._query_active_rounds()
            .order_by(Round.id.asc())
            .first()
        )
