import math
from typing import Tuple
from maths import v_truncate, w_truncate, Gaussian
from trueskill import PERFORMANCE_NOISE, DYNAMIC_FACTOR


def update_rating(winner: Gaussian, loser: Gaussian,
                  perf_noise_sigma=PERFORMANCE_NOISE,
                  dynamics_factor=DYNAMIC_FACTOR) -> Tuple[Gaussian, Gaussian]:
    """Updates the skills of two players in a 1vs1 match.

    Args:
        winner: Skill of the winner
        loser: Skill of the loser
        perf_noise_sigma: The standard devication of the performance noise.
        dynamics_factor: The standard deviation of the dynamics factor on the
        prior skill which allows uncertainty in skill to vary over time.

    Returns:
        Two new Gaussian objects containing the updated winner skill and
        updated loser skill respectively.
    """
    c = math.sqrt(winner.sigma ** 2 + loser.sigma ** 2 +
                  2 * perf_noise_sigma ** 2)
    winner_adjusted_var = winner.sigma**2 + dynamics_factor**2
    loser_adjusted_var = loser.sigma**2 + dynamics_factor**2

    winning_mu = winner.mu
    losing_mu = loser.mu
    delta_mu = winning_mu - losing_mu

    # calculate the additive and multiplicative correction factors
    v_game = v_truncate(delta_mu / c)
    w_game = w_truncate(delta_mu / c)

    # update the winner
    mu_multiplier = winner_adjusted_var / c
    sigma_multiplier = winner_adjusted_var / c**2
    new_mu = winning_mu + mu_multiplier * v_game
    new_sigma = math.sqrt(winner_adjusted_var*(1-w_game*sigma_multiplier))
    updated_winner = Gaussian(mu=new_mu, sigma=new_sigma)

    # update the loser
    mu_multiplier = loser_adjusted_var / c
    sigma_multiplier = loser_adjusted_var / c**2
    new_mu = losing_mu - mu_multiplier * v_game
    new_sigma = math.sqrt(loser_adjusted_var*(1-w_game*sigma_multiplier))
    updated_loser = Gaussian(mu=new_mu, sigma=new_sigma)

    return updated_winner, updated_loser






