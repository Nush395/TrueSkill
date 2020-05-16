from scipy.stats.distributions import norm
import math


def V(x: float) -> float:
    return norm.pdf(x) / norm.cdf(x)


def W(x: float) -> float:
    return V(x)*(x+V(x))


class Gaussian:
    """Class to act as a container to hold parameters for Gaussians
    maybe this can be replaced with a named tuple
    """
    def __init__(self, mu=None, sigma=None, pi=None, tau=None):
        if pi is not None and tau is not None:
            self.pi = pi
            self.tau = tau
            self.sigma = self.pi ** -2
            self.mu = self.tau / self.pi
        elif mu is not None and sigma is not None:
            self.pi = sigma ** -2
            self.tau = self.pi * mu
            self.mu = mu
            self.sigma = sigma
        else:
            self.pi = self.tau = self.mu = 0
            self.sigma = None

    def __mul__(self, other):
        if not isinstance(other, Gaussian):
            raise TypeError("Attempt to multiply a Gaussian by something not Gaussian!")
        return Gaussian(pi=self.pi+other.pi, tau=self.tau+other.tau)

    def __truediv__(self, other):
        if not isinstance(other, Gaussian):
            raise TypeError("Attempt to divide a Gaussian by something not Gaussian!")
        return Gaussian(pi=self.pi-other.pi, tau=self.tau-other.tau)

    def __repr__(self):
        return f"Gaussian(mu={self.mu}, sigma={self.sigma})"

    def __eq__(self, other):
        if other.mu == self.mu and other.sigma == self.sigma:
            return True
        else:
            return False



