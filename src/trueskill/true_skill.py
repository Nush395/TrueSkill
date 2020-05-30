from typing import List, Dict
from src.utils.maths import Gaussian
from src.trueskill.constants import DYNAMIC_FACTOR, PERFORMANCE_NOISE, DELTA
from src.trueskill.factor_graph import Variable, PerformanceFactor, PriorFactor,\
    SumFactor, TruncateFactor


class TrueSkill:
    def __init__(self, teams: List[Dict[str, Gaussian]],
                 dynamics=DYNAMIC_FACTOR,
                 perf_noise_sigma=PERFORMANCE_NOISE,
                 delta=DELTA):
        """Builds and runs a TrueSkill environment.

        Args:
            teams: List of the team skills sorted in the order they ranked.
            dynamics: The standard deviation on the prior skill which allows
            the skill to vary over time.
            perf_noise_sigma: The standard deviation of the performance noise.
            delta: The minimum difference two marginals have to satisfy to be
            considered approximately equal (for the approximation of game
            marginals.)
        """
        self.dynamics = dynamics
        self.perf_sigma = perf_noise_sigma
        self.delta = delta
        self.teams = teams
        self.players = []
        self.prior_factors = []
        self.perf_factors = []
        self.team_factors = []
        self.truncate_factors = []
        self._build()

    def _build(self):
        """Builds the relevant factor graph for this TrueSkill environment
        for the game information given"""
        team_vars = []
        for team in self.teams:
            team_var = Variable()
            team_vars.append(team_var)
            performance_vars = []
            for player in team:
                player_var = Variable(name=player)
                self.players.append(player_var)
                prior_factor = PriorFactor(player_var, team[player])
                self.prior_factors.append(prior_factor)
                performance_var = Variable()
                perf_factor = PerformanceFactor(player_var, performance_var)
                self.perf_factors.append(perf_factor)
                performance_vars.append(performance_var)
            team_factor = SumFactor(team_var, performance_vars,
                                    [1.0]*len(performance_vars))
            self.team_factors.append(team_factor)
        game_vars = [Variable() for _ in range(len(self.teams)-1)]
        self.game_factors = [SumFactor(game_var,
                                       [team_vars[i], team_vars[i+1]],
                                       [1, -1])
                             for i, game_var in enumerate(game_vars)]
        self.truncate_factors = [TruncateFactor(game_var)
                                 for game_var in game_vars]

    def _run(self):
        """Run the built factor graph and update skills with posteriors using
        the schedule described in the original paper."""
        for factor in self.prior_factors:
            factor.down()
        for factor in self.perf_factors:
            factor.down()
        for factor in self.team_factors:
            factor.down()
        if len(self.teams) > 2:
            # iterate till approximate game outcome marginals don't change
            while True:
                delta = 0
                for i in range(len(self.game_factors)-1):
                    self.game_factors[i].down()
                    delta = max(delta, self.truncate_factors[i].up())
                    self.game_factors[i].up(1)
                    self.game_factors[i+1].down()
                    delta = max(delta, self.truncate_factors[i+1].up())
                    self.game_factors[i+1].up(0)
                if delta <= self.delta:
                    break
        else:
            self.game_factors[0].down()
            self.truncate_factors[0].up()
        self.game_factors[0].up(0)
        self.game_factors[-1].up(1)
        for team_factor in self.team_factors:
            # no. of player variables = total variables - team variable
            num_players = len(team_factor.vars) - 1
            for player_num in range(num_players):
                team_factor.up(player_num)
        for perf_factor in self.perf_factors:
            perf_factor.up()

    def update_ratings(self):
        self._run()  # run the message passing algorithm
        new_ratings = {}
        for player in self.players:
            name = player.name
            pi = player.pi
            tau = player.tau
            new_ratings[name] = Gaussian(pi=pi, tau=tau)

        return new_ratings



            



