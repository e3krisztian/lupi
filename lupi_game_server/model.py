from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    votes = db.relationship("Vote", backref="round", lazy=True)

    @property
    def is_completed(self):
        return self.end_date is not None

    def get_winner(self):
        collector = defaultdict(list)
        for vote in self.votes:
            collector[vote.number].append(vote)
        for number, votes in sorted(collector.items()):
            if len(votes) == 1:
                return votes[0]


class Vote(db.Model):
    __table_args__ = tuple([db.UniqueConstraint('round_id', 'name')])

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    round_id = db.Column(db.ForeignKey('round.id'), nullable=False)
