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


def test_make_round_fails_when_there_is_an_active_round(db):
    game.make_round()
    with pytest.raises(game.Error):
        game.make_round()


def test_make_round_round_ids_autoincrement(db):

    r1 = game.make_round()
    game.complete_round()

    r2 = game.make_round()
    game.complete_round()

    r3 = game.make_round()
    game.complete_round()

    assert r1.id < r2.id < r3.id  # id autoincrement


def test_get_current_round_id(db):
    round = game.make_round()
    assert round.id == game.get_current_round_id()


def test_get_current_round_id_no_rounds_at_all(db):
    with pytest.raises(LookupError):
        game.get_current_round_id()


def test_get_current_round_id_when_there_are_no_active_rounds(db):
    round = game.make_round()
    game.complete_round()

    with pytest.raises(LookupError):
        game.get_current_round_id()


def test_complete_round(db):
    r = game.make_round()
    assert not r.is_completed

    game.complete_round()

    assert r.is_completed


def test_complete_round_sets_end_date(db):
    r = game.make_round()
    assert not r.is_completed

    game.complete_round()

    assert r.end_date != None


def test_add_votes(db):
    game.make_round()
    game.add_vote('name1', 1)
    game.add_vote('name2', 1)
    game.add_vote('name3', 2)


def test_add_vote_no_current_round(db):
    with pytest.raises(game.Error):
        game.add_vote('name', 1)


def test_add_vote_duplicate_name(db):
    game.make_round()
    game.add_vote('name', 1)
    with pytest.raises(game.Error):
        game.add_vote('name', 2)


def test_get_current_round_id_when_there_are_multiple_active_is_selected_by_id(db):
    """ Having multiple active rounds is invalid state for the game.

    This might happen however in practice.
    The stable solutions are:
    select the one with the smallest id or select the one with the largest id.
    We force the smallest id in this test.
    """
    r1 = _make_round_directly(db)
    _make_round_directly(db)

    assert game.get_current_round_id() == r1.id


def test_complete_round_works_only_on_current_round(db):
    """ This is a data anomaly cleanup function, we should have only one open round.
    """
    _make_round_directly(db)
    _make_round_directly(db)

    game.complete_round()

    with pytest.raises(LookupError):
        game.get_current_round_id()


def test_complete_round_closes_all_other_open_rounds(db):
    """ This is a data anomaly cleanup function, we should have only one open round.
    """
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
