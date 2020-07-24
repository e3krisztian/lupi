"""
Game data.

Caveat: this implementation potentially leads to data anomalies
due to concurrent usage.

---

While preventing the anomalies is possible, it is hard.
Testing that anomalies are not created is also hard.

Having multiple actors changing data concurrently can result in
race conditions, which are very hard to test, so it is outside
the scope of this project.
(Testing race conditions programmatically is interesting,
it usually involves some advanced technique, like instrumenting
the code or tracing through it like a debugger, e.g. could be
made similarly to how ThreadWeaver for Java works
https://youtu.be/FvH4RBn2gJ8)

One solution to this problem is to prevent the anomalies occuring.
(e.g. have all high level game operations atomic and serialized)

Another solution is to live with the anomalies occuring and test
code against data anomalies.

---
Voting for a round is not allowed after a round is closed,
because it allows the last voter to influence the round result.

However
- closing the round
- adding a new vote
in parallel can result in closing first, then voting.

Voting can start earlier, than the round closing and finish later.
In fact another results can be faster than the last vote, so
the result without the last vote can be shown to players.

Options to cut through this problem:
- do not care: it will be eventually consistent
- serialize db transactions somehow
  (e.g. use SQL WITH FOR UPDATE to make a write lock on rounds in vote)

As it would go untested, the real world impact is almost none
(not for money game) and the problem would occur rarely,
the first option was chosen.

---
Voting with the same name[s] in parallel.

In this case the choices are:
- allowing it to happen, which would eventually make the round invalid
- prevent it by not allowing one of the votes.

It is an easy to solve problem with
databases: a unique constraint can take care of preventing the second
vote to succeed.

---
Opening multiple rounds in parallel is another similarly
hard to prevent/test problem.
It can result in some votes lost, and unclosed rounds.
To minimize the impact of having multiple rounds open:
- care must be taken to select the active round unambiguously
  (e.g. smallest by id)
- closing a round should also close all other unclosed rounds
  to prevent having an open round immediately after closing
  the current one (the other unclosed round)
"""

###
RoundId = int

class GameData:
    def current_round() -> RoundId:
        pass

    def new_round() -> RoundId:
        pass

    def complete_round(round_id: RoundId):
        pass

    def add_vote(round_id: RoundId, name, number):
        pass
