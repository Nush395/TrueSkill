import math
from typing import Tuple
from maths import V, W, Gaussian


def update_rating(winner: Gaussian, loser: Gaussian,
                  perf_noise_sigma=25/6,
                  dynamics_factor=0) -> Tuple[Gaussian, Gaussian]:
    """

    :param winner:
    :param loser:
    :param perf_noise_sigma:
    :param dynamics_factor:
    :return:
    """
    c = math.sqrt(winner.sigma ** 2 + loser.sigma ** 2 +
                  2 * perf_noise_sigma ** 2)
    winner_adjusted_var = winner.sigma**2 + dynamics_factor**2
    loser_adjusted_var = loser.sigma**2 + dynamics_factor**2

    winning_mu = winner.mu
    losing_mu = loser.mu
    delta_mu = winning_mu - losing_mu

    # calculate the additive and multiplicative correction factors
    v_game = V(delta_mu/c)
    w_game = W(delta_mu/c)

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






