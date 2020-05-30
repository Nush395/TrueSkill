import math
from src.utils.maths import Gaussian, v_truncate, w_truncate
from typing import List
from abc import ABC, abstractmethod
from src.trueskill.constants import PERFORMANCE_NOISE, DYNAMIC_FACTOR


class Factor(ABC):
    def __init__(self, variables):
        self.vars = variables
        for var in self.vars:
            var.messages[self] = Gaussian()

    @abstractmethod
    def down(self):
        pass

    @abstractmethod
    def up(self):
        pass


class Variable(Gaussian):
    def __init__(self, name=""):
        # each entry in the messages dict is a factor whose value is the
        # message from that factor to this variable
        self.messages = {}
        self.name = name
        super().__init__()

    @property
    def marginal(self):
        return Gaussian(pi=self.pi, tau=self.tau)

    @marginal.setter
    def marginal(self, val: Gaussian):
        self.pi = val.pi
        self.tau = val.tau

    def update_message(self, factor: Factor, message: Gaussian):
        # update the factor to variable message
        old_message, self.messages[factor] = self.messages[factor], message
        self.marginal = self / old_message * message

    def update_marginal(self, factor: Factor, value: Gaussian):
        old_message = self.messages[factor]
        self.messages[factor] = value * old_message / self
        self.marginal = value


class PriorFactor(Factor):
    def __init__(self, variable: Variable, value: Gaussian,
                 dynamic=DYNAMIC_FACTOR):
        super().__init__([variable])
        self.var = variable
        self.value = value
        self.dynamic = dynamic

    def down(self):
        pi = 1 / (self.value.pi ** -1 + self.dynamic ** 2)
        value = Gaussian(pi=pi, tau=self.value.tau)
        self.var.update_marginal(self, value)

    def up(self):
        return 0


class PerformanceFactor(Factor):
    def __init__(self, mean: Variable, performance: Variable,
                 beta=PERFORMANCE_NOISE):
        super().__init__([mean, performance])
        self.beta = beta
        self.mean_skill = mean
        self.performance = performance

    def _update_helper(self, variable_one: Variable, variable_two: Variable):
        msg = variable_one / variable_one.messages[self]
        a = 1 / (1 + self.beta ** 2 * msg.pi)
        message = Gaussian(pi=a*msg.pi, tau=a*msg.tau)
        variable_two.update_message(self, message)

    def down(self):
        self._update_helper(self.mean_skill, self.performance)

    def up(self):
        self._update_helper(self.performance, self.mean_skill)


class SumFactor(Factor):
    def __init__(self, sum_var: Variable, perf_vars: List[Variable],
                 coeffs: List[float]):
        super().__init__([sum_var] + perf_vars)
        self.perf_vars = perf_vars
        self.sum_var = sum_var
        self.coeffs = coeffs

    def _update_helper(self, var: Variable, perf_vars: List[Variable],
                       perf_messages: List[Gaussian], coeffs: List[float]):
        # TODO: Make variables, messages and coeffs a list of named tuples.
        assert len(perf_vars) == len(perf_messages) == len(coeffs)
        pi = 1.0 / sum([coeffs[i]**2 / (perf_vars[i].pi - perf_messages[i].pi)
                        for i in range(len(coeffs))])
        tau = pi * sum([coeffs[i] *
                        (perf_vars[i].tau - perf_messages[i].tau) /
                        (perf_vars[i].pi - perf_messages[i].pi)
                        for i in range(len(coeffs))])
        new_message = Gaussian(pi=pi, tau=tau)
        var.update_message(self, new_message)

    def up(self, idx=0):
        variables = ([var for i, var in enumerate(self.perf_vars) if i != idx]
                     + [self.sum_var])
        messages = [var.messages[self] for var in variables]
        coeffs = [- (self.coeffs[i] / self.coeffs[idx])
                  for i in range(len(self.coeffs))
                  if i != idx]
        coeffs += [1.0 / self.coeffs[idx]]
        self._update_helper(self.perf_vars[idx], variables, messages, coeffs)

    def down(self):
        messages = [var.messages[self] for var in self.perf_vars]
        self._update_helper(self.sum_var, self.perf_vars, messages,
                            self.coeffs)


class TruncateFactor(Factor):
    def __init__(self, variable: Variable):
        super().__init__([variable])
        self.var = variable

    def up(self):
        c = self.var.pi - self.var.messages[self].pi
        d = self.var.tau - self.var.messages[self].tau
        pi = c / (1-w_truncate(d / math.sqrt(c)))
        tau = ((d + math.sqrt(c) * v_truncate(d / math.sqrt(c))) /
               (1 - w_truncate(d / math.sqrt(c))))
        old_marginal = self.var.marginal
        self.var.update_marginal(self, Gaussian(pi=pi, tau=tau))
        return old_marginal.kl_divergence(self.var.marginal)

    def down(self):
        return 0

