## TrueSkill module
This module contains the components that implement the TrueSkill algorithm. If you're starting out as I was then the two_player and
two_team implementations are easier to follow initially.

### true_skill.py
Contains the core TrueSkill environment that can be instantiated and used to update player ratings in a game.

### factor_graph.py
Contains the Variable and Factor nodes that comprise the factor graph for TrueSkill.

### true_skill_two_player.py
Explicitly written out two player case skill updates, I used to help me when I was understanding the algorithm.

### true_skill_two_teams.py
Similar to the above, an explicitly written skill update for players in a two team game.
