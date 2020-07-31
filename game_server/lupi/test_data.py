from datetime import datetime
import pytest

from . import data as game
from .model import Round


class Test_get_round:
    def test_no_current_round(self, db):
        assert game.get_round("current") is None

    def test_no_round_with_id(self, db):
        assert game.get_round("1") is None

    def test_current(self, db):
        round = game.make_round()
        assert game.get_round("current") == round

    def test_with_id(self, db):
        round = game.make_round()
        assert game.get_round(round.id) == round
        assert game.get_round(str(round.id)) == round

    def test_completed_with_id(self, db):
        round = game.make_round()
        game.complete_round()
        assert game.get_round(round.id) == round
        assert game.get_round(str(round.id)) == round


class Test_make_round:

    def test_fails_when_there_is_an_active_round(self, db):
        game.make_round()
        with pytest.raises(game.Error):
            game.make_round()

    def test_round_ids_autoincrement(self, db):

        r1 = game.make_round()
        game.complete_round()

        r2 = game.make_round()
        game.complete_round()

        r3 = game.make_round()
        game.complete_round()

        assert r1.id < r2.id < r3.id  # id autoincrement


class Test_get_current_round_id:

    def test_happy_path(self, db):
        round = game.make_round()
        assert round.id == game.get_current_round_id()

    def test_no_rounds_at_all(self, db):
        with pytest.raises(LookupError):
            game.get_current_round_id()

    def test_when_there_are_no_active_rounds(self, db):
        round = game.make_round()
        game.complete_round()

        with pytest.raises(LookupError):
            game.get_current_round_id()


class Test_complete_round:

    def test_happy_path(self, db):
        r = game.make_round()
        assert not r.is_completed

        game.complete_round()

        assert r.is_completed

    def test_sets_end_date(self, db):
        r = game.make_round()
        assert not r.is_completed

        game.complete_round()

        assert r.end_date != None


class Test_add_vote:

    def test_happy_path(self, db):
        game.make_round()
        game.add_vote('name1', 1)
        game.add_vote('name2', 1)
        game.add_vote('name3', 2)

    def test_no_current_round(self, db):
        with pytest.raises(game.Error):
            game.add_vote('name', 1)

    def test_duplicate_name(self, db):
        game.make_round()
        game.add_vote('name', 1)
        with pytest.raises(game.Error):
            game.add_vote('name', 2)


class Test_data_anomaly:
    """ Tests related to having multiple active rounds.
    
    It is an invalid state for the game.
    This might happen however in practice.

    Tests here are related to handling the anomaly if present.
    """

    def test_get_current_round_id(self, db):
        """Select the one with the smallest id."""
        r1 = _make_round_directly(db)
        _make_round_directly(db)

        assert game.get_current_round_id() == r1.id

    def test_complete_round(self, db):
        """Close all other open rounds as well."""
        _make_round_directly(db)
        _make_round_directly(db)

        game.complete_round()

        with pytest.raises(LookupError):
            game.get_current_round_id()


def _make_round_directly(db):
    r = Round(start_date=datetime.utcnow())
    db.session.add(r)
    db.session.flush()
    return r
