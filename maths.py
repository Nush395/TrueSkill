from scipy.stats.distributions import norm
import math
import logging


def v_truncate(x: float) -> float:
    """Computes the additive correction term to the moment matching
    approximation of the truncated Gaussian as detailed in original paper.
    """
    return norm.pdf(x) / norm.cdf(x)


def w_truncate(x: float) -> float:
    """Helper to compute the multiplicative correction term to the moment
    matching approximation of the truncated Gaussian as detailed in original
    paper.
    """
    return v_truncate(x) * (x + v_truncate(x))


class Gaussian:
    """Class to act as a container to hold parameters for Gaussians."""
    def __init__(self, mu=None, sigma=None, pi=None, tau=None):
        if pi is not None and tau is not None:
            self.pi = pi
            self.tau = tau
        # sigma must be both not None and non-zero
        elif mu is not None and sigma:
            self.pi = sigma ** -2
            self.tau = self.pi * mu
        else:
            self.pi = self.tau = 0

    def __mul__(self, other):
        if not isinstance(other, Gaussian):
            raise TypeError("Attempt to multiply a Gaussian by something not Gaussian!")
        return Gaussian(pi=self.pi+other.pi, tau=self.tau+other.tau)

    def __truediv__(self, other):
        if not isinstance(other, Gaussian):
            raise TypeError("Attempt to divide a Gaussian by something not Gaussian!")
        return Gaussian(pi=self.pi-other.pi, tau=self.tau-other.tau)

    def __repr__(self):
        if self.pi:
            sigma = 1/math.sqrt(self.pi)
            mu = self.tau/self.pi
        else:
            sigma = "inf"
            mu = 0

        return f"Gaussian(mu={mu}, sigma={sigma})"

    def __eq__(self, other):
        if other.pi == self.pi and other.tau == self.tau:
            return True
        else:
            return False

    @property
    def mu(self):
        if self.pi != 0:
            return self.tau / self.pi
        else:
            return 0

    @mu.setter
    @property
    def mu(self, mu):
        self.tau = self.pi * mu

    @property
    def sigma(self):
        if self.pi > 0:
            return 1 / math.sqrt(self.pi)
        elif self.pi == 0:
            logging.warning("Standard deviation of this Gaussian is infinite.")
            return float('inf')
        else:
            logging.error("Precision of this Gaussian is not well defined.")
            raise ValueError("Ill-defined precision.")

    @sigma.setter
    @property
    def sigma(self, sigma):
        self.pi = 1 / math.sqrt(sigma)






