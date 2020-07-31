from datetime import datetime
import pytest

from .data import GameData
from .model import Round


def test_make_round_fails_when_there_is_an_active_round(db):
    gd = GameData()
    gd.make_round()

    with pytest.raises(GameData.Error):
        gd.make_round()


def test_make_round_round_ids_autoincrement(db):
    gd = GameData()

    r1 = gd.make_round()
    gd.complete_round()

    r2 = gd.make_round()
    gd.complete_round()

    r3 = gd.make_round()
    gd.complete_round()

    assert r1.id < r2.id < r3.id  # id autoincrement


def test_get_current_round_id(db):
    gd = GameData()
    round = gd.make_round()
    assert round.id == gd.get_current_round_id()


def test_get_current_round_id_no_rounds_at_all(db):
    with pytest.raises(LookupError):
        GameData().get_current_round_id()


def test_get_current_round_id_when_there_are_no_active_rounds(db):
    gd = GameData()
    round = gd.make_round()
    gd.complete_round()

    with pytest.raises(LookupError):
        GameData().get_current_round_id()


def test_complete_round(db):
    gd = GameData()
    r = gd.make_round()
    assert not r.is_completed

    gd.complete_round()

    assert r.is_completed


def test_complete_round_sets_end_date(db):
    gd = GameData()
    r = gd.make_round()
    assert not r.is_completed

    gd.complete_round()

    assert r.end_date != None


def test_add_votes(db):
    gd = GameData()
    gd.make_round()
    gd.add_vote('name1', 1)
    gd.add_vote('name2', 1)
    gd.add_vote('name3', 2)


def test_add_vote_no_current_round(db):
    gd = GameData()
    with pytest.raises(GameData.Error):
        gd.add_vote('name', 1)


def test_add_vote_duplicate_name(db):
    gd = GameData()
    gd.make_round()
    gd.add_vote('name', 1)
    with pytest.raises(GameData.Error):
        gd.add_vote('name', 2)


def test_get_current_round_id_when_there_are_multiple_active_is_selected_by_id(db):
    """ Having multiple active rounds is invalid state for the game.

    This might happen however in practice.
    The stable solutions are:
    select the one with the smallest id or select the one with the largest id.
    We force the smallest id in this test.
    """
    r1 = _make_round_directly(db)
    _make_round_directly(db)

    assert GameData().get_current_round_id() == r1.id


def test_complete_round_works_only_on_current_round(db):
    """ This is a data anomaly cleanup function, we should have only one open round.
    """
    _make_round_directly(db)
    _make_round_directly(db)

    gd = GameData()
    gd.complete_round()

    with pytest.raises(LookupError):
        gd.get_current_round_id()


def test_complete_round_closes_all_other_open_rounds(db):
    """ This is a data anomaly cleanup function, we should have only one open round.
    """
    _make_round_directly(db)
    _make_round_directly(db)

    gd = GameData()
    gd.complete_round()

    with pytest.raises(LookupError):
        gd.get_current_round_id()


def _make_round_directly(db):
    r = Round(start_date=datetime.utcnow())
    db.session.add(r)
    db.session.flush()
    return r
