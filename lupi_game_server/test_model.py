from enum import unique
from .model import Round, Vote

import pytest


@pytest.fixture
def round():
    round = Round()
    yield round

def add_vote(round, name, number):
    round.votes.append(Vote(name=name, number=number))


class Test_get_winner:
    def test_no_votes(self, round):
        winner = round.get_winner()

        assert not winner

    def test_duplicate_votes(self, round):
        add_vote(round, "name1", 1)
        add_vote(round, "name2", 1)

        winner = round.get_winner()

        assert not winner

    def test_single_vote(self, round):
        add_vote(round, "winner", 42)

        winner = round.get_winner()

        assert winner.name == "winner"
        assert winner.number == 42

    def test_unique_between_duplicates(self, round):
        add_vote(round, "name1", 1)
        add_vote(round, "name2", 1)
        add_vote(round, "winner", 42)
        add_vote(round, "name11", 100)
        add_vote(round, "name22", 100)

        winner = round.get_winner()

        assert winner.name == "winner"
        assert winner.number == 42

    def test_multiple_unique(self, round):
        add_vote(round, "name1", 1)
        add_vote(round, "name2", 1)
        add_vote(round, "winner", 42)
        add_vote(round, "loser", 43)
        add_vote(round, "name11", 100)
        add_vote(round, "name22", 100)

        winner = round.get_winner()

        assert winner.name == "winner"
        assert winner.number == 42
