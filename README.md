# Lupi

Least Unique Positive Integer is a fun game and now that people are stuck in home office it can be a great way to have to start the day with a common activity. The game has been studied a lot and has some maths behind how people behave and what really is optimal in some respect.


## Game Rules

It is a Multiplayer game, each player picks a positive integer. The lowest unique integer wins.


## Implementation

Focus is on the API that enables this game service and only provide a very basic GUI.


### Plan

1. Specify a Restful API for a simple variant of the problem using the Minimum Features.
2. Implement this using Flask/Python.
3. Iterate 1 and 2 adding some of the Extra features
4. Provide a basic web UI.


### Minimum Features:

- Single Global Playground
- Trusted players (no registration)
- Explicit start of a round
- Within an active round:
  - A user can add their number with a name as part of the game. The name is unique and cannot be reused in the round.
  - All users vote is collected.
- Complete the Round, return round_id
- Round Results: winner, and the number
- Listing all rounds with IDs and start date, end date, number of participants
- Querying the results of any rounds including the most recent one: winner and winning number
- Querying the statistics of any round: distribution of votes from 1 to the max number voted for in that round.


### Extra Features:

- Groups to isolate playgrounds within which the rounds of votes happen.
- Group admin can create/invite group members or people can request membership and that is approved by the Group admin
- Auto Round Close
- Login/auth
- Avatar upload for people
- Group Admin can request Group Stats but nobody else.
- Global Admin can list all groups and request Stats of any Groups.
- Global Admin can run global stats (aggregated for all group)
- Stats may make sense to break down by the number of participants. Consider that too
- More advanced GUI with stats.
