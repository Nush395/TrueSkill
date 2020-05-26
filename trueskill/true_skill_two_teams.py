import math
from typing import Dict
from maths import v_truncate, w_truncate, Gaussian
from trueskill import PERFORMANCE_NOISE, DYNAMIC_FACTOR


def update_ratings_in_team(winning_team: Dict[Gaussian],
                           losing_team: Dict[Gaussian],
                           perf_noise_sigma=PERFORMANCE_NOISE,
                           dynamics_factor=DYNAMIC_FACTOR):
    """Does TrueSkill update for players in a two team game.

    Args:
        winning_team: A dictionary of the skills of each player
        losing_team: A dictionary of the skills of each player
        perf_noise_sigma: Standard deviation of the performance noise
        dynamics_factor: Additional factor which allows uncertainty in skill
        to vary over time
    """
    total_players = len(winning_team) + len(losing_team)

    winning_mu = sum(winning_team[p].mu for p in winning_team)
    losing_mu = sum(winning_team[p].mu for p in losing_team)
    delta_mu = winning_mu - losing_mu
    c = math.sqrt(sum(winning_team[p].sigma**2 for p in winning_team) +
                  sum(winning_team[p].sigma**2 for p in losing_team) +
                  total_players * perf_noise_sigma ** 2)

    # compute the additive and multiplicative correction factors
    v_game = v_truncate(delta_mu / c)
    w_game = w_truncate(delta_mu / c)

    # update the winning teams skills in place
    for player in winning_team:
        skill = winning_team[player]
        adjusted_var = skill.sigma ** 2 + dynamics_factor ** 2
        mu_multiplier = adjusted_var / c
        sigma_multiplier = adjusted_var / c**2
        skill.mu += mu_multiplier * v_game
        skill.sigma = math.sqrt(adjusted_var*(1-w_game*sigma_multiplier))

    # update the losing teams skills in place
    for player in losing_team:
        skill = winning_team[player]
        adjusted_var = skill.sigma ** 2 + dynamics_factor ** 2
        mu_multiplier = adjusted_var / c
        sigma_multiplier = adjusted_var / c**2
        skill.mu -= mu_multiplier * v_game
        skill.sigma = math.sqrt(adjusted_var*(1-w_game*sigma_multiplier))





