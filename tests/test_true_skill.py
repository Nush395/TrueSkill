import unittest
from unittest.mock import patch
from trueskill.engine.true_skill_two_player import update_rating
from trueskill.engine.true_skill_two_teams import update_ratings_in_team
from trueskill.engine.true_skill import TrueSkillEnv
from trueskill.utils.constants import MU, SIGMA
from trueskill.utils.maths import Gaussian
from trueskill.engine.factor_graph import Variable, PriorFactor, \
    PerformanceFactor, TruncateFactor, SumFactor


class TestTrueSkill(unittest.TestCase):
    def test_factor_graph_agrees_with_two_player_explicit(self):
        # given
        winner = Gaussian(mu=MU, sigma=SIGMA)
        loser = Gaussian(mu=MU, sigma=SIGMA)
        teams = [{"winner": winner}, {"loser": loser}]

        # when
        # we update the skills with the analytic method
        updated_winner, updated_loser = update_rating(winner, loser)
        # and we update the skills with the factor graph
        ts = TrueSkillEnv(teams)
        new_ratings = ts.update_ratings()

        # then
        # expect the results to be almost equal due to floating point errors
        # TODO check that this level of error is expected.
        self.assertAlmostEqual(new_ratings["winner"].mu, updated_winner.mu, 2)
        self.assertAlmostEqual(new_ratings["loser"].mu, updated_loser.mu, 2)
        self.assertAlmostEqual(new_ratings["winner"].sigma,
                               updated_loser.sigma, 2)
        self.assertAlmostEqual(new_ratings["loser"].sigma,
                               updated_loser.sigma, 2)

    def test_factor_graph_agrees_with_two_team_explicit(self):
        # given
        p1 = Gaussian(mu=MU, sigma=SIGMA)
        p2 = Gaussian(mu=MU, sigma=SIGMA)
        p3 = Gaussian(mu=MU, sigma=SIGMA)
        losing_team = {"player3": p3, "player2": p2}
        winning_team = {"player1": p1}
        teams = [winning_team] + [losing_team]

        # when
        # we update skills with the factor graph
        ts = TrueSkillEnv(teams)
        new_ratings = ts.update_ratings()
        # and update skills with the analytic method
        update_ratings_in_team(winning_team, losing_team)

        # then
        self.assertAlmostEqual(new_ratings["player1"].mu,
                               winning_team["player1"].mu, 2)
        self.assertAlmostEqual(new_ratings["player2"].mu,
                               losing_team["player2"].mu, 2)
        self.assertAlmostEqual(new_ratings["player3"].mu,
                               losing_team["player3"].mu, 2)
        self.assertAlmostEqual(new_ratings["player1"].sigma,
                               winning_team["player1"].sigma, 2)
        self.assertAlmostEqual(new_ratings["player2"].sigma,
                               new_ratings["player2"].sigma, 2)
        self.assertAlmostEqual(new_ratings["player3"].sigma,
                               losing_team["player3"].sigma, 2)

    def test_three_team_converges(self):
        # given
        p1 = Gaussian(mu=MU, sigma=SIGMA)
        p2 = Gaussian(mu=MU, sigma=SIGMA)
        p3 = Gaussian(mu=MU, sigma=SIGMA)
        teams = [{"player1": p1}, {"player2": p2}, {"player3": p3}]

        # when
        ts = TrueSkillEnv(teams)
        ts.update_ratings()

        # then expect a convergence


class TestFactorGraph(unittest.TestCase):
    def test_prior_factor_down(self):
        # given
        var = Variable("player1")
        dyn_fact = 0.5
        val = Gaussian(mu=MU, sigma=SIGMA)
        pf = PriorFactor(var, val, dyn_fact)

        # when
        pf.down()

        # then
        expected_pi = 1 / (SIGMA ** 2 + dyn_fact ** 2)
        expected_marginal = Gaussian(pi=expected_pi, tau=val.tau)
        self.assertEqual(expected_marginal, pf.var.marginal)

    @patch("trueskill.engine.factor_graph.PerformanceFactor._update_helper")
    def test_performance_factor_down(self, mock_update):
        # given
        val1 = Variable()
        val2 = Variable()
        pf = PerformanceFactor(val1, val2)

        # when
        pf.down()

        # then
        mock_update.assert_called_with(val1, val2)

    @patch("trueskill.engine.factor_graph.PerformanceFactor._update_helper")
    def test_performance_factor_up(self, mock_update):
        # given
        val1 = Variable()
        val2 = Variable()
        pf = PerformanceFactor(val1, val2)

        # when
        pf.down()

        # then
        mock_update.assert_called_with(val2, val1)

    def test_sum_factor_helper(self):
        # given
        var = Variable()
        var1, var2 = Variable(), Variable()
        var1.pi, var2.pi, var1.tau, var2.tau = [1] * 4
        perf_vars = [var1, var2]
        perf_messages = [Gaussian(), Gaussian()]
        coeffs = [1,2]
        sf = SumFactor(var, perf_vars, coeffs)

        # when
        sf._update_helper(var, perf_vars, perf_messages, coeffs)

        # then
        expected_pi = 1 / (1/1 + 1/2)
        expected_tau = expected_pi * (1 + 2)
        var.messages[sf] = Gaussian(pi=expected_pi, tau=expected_tau)

    @patch("trueskill.engine.factor_graph.SumFactor._update_helper")
    def test_sum_factor_down(self, mock_helper):
        # given
        var = Variable()
        var1, var2 = Variable(), Variable()
        var1.pi, var2.pi, var1.tau, var2.tau = [1] * 4
        perf_vars = [var1, var2]
        perf_messages = [Gaussian(), Gaussian()]
        coeffs = [1,2]
        sf = SumFactor(var, perf_vars, coeffs)

        # when
        sf.down()

        # then
        expected_messages = [var1.messages[sf], var2.messages[sf]]
        mock_helper.assert_called_with(var, perf_vars, expected_messages,
                                       coeffs)

    @patch("trueskill.engine.factor_graph.SumFactor._update_helper")
    def test_sum_factor_up(self, mock_helper):
        # given
        var = Variable()
        var1, var2 = Variable(), Variable()
        var1.pi, var2.pi, var1.tau, var2.tau = [1] * 4
        perf_vars = [var1, var2]
        perf_messages = [Gaussian(), Gaussian()]
        coeffs = [1,2]
        sf = SumFactor(var, perf_vars, coeffs)

        # when
        sf.up(0)

        # then
        # expect all variables except that at index 0
        expected_vars = [var2, var]
        expected_messages = [var2.messages[sf], var.messages[sf]]
        expected_coeffs = [-2, 1]  # coefficients of rearranged equation
        mock_helper.assert_called_with(var1, expected_vars, expected_messages,
                                       expected_coeffs)

    @patch("trueskill.utils.maths.Gaussian.kl_divergence")
    @patch("trueskill.engine.factor_graph.w_truncate", return_value=0)
    @patch("trueskill.engine.factor_graph.v_truncate", return_value=0)
    def test_truncate_factor_updates_marginal(self, mock_v, mock_w, mock_kl):
        # given
        var = Variable()
        var.pi, var.tau = [1]*2
        tf = TruncateFactor(var)

        # when
        tf.up()

        # then
        expected_tau = 1
        expected_pi = 1
        expected_marginal = Gaussian(pi=expected_pi, tau=expected_tau)
        self.assertEqual(var.marginal, expected_marginal)

    @patch("trueskill.utils.maths.Gaussian.kl_divergence")
    @patch("trueskill.engine.factor_graph.w_truncate", return_value=0)
    @patch("trueskill.engine.factor_graph.v_truncate", return_value=0)
    def test_truncate_factor_calls_kl_divergence(self, mock_v, mock_w, mock_kl):
        # given
        var = Variable()
        var.pi, var.tau = [1]*2
        tf = TruncateFactor(var)

        # when
        tf.up()

        # then
        expected_tau = 1
        expected_pi = 1
        expected_marginal = Gaussian(pi=expected_pi, tau=expected_tau)
        mock_kl.assert_called_with(expected_marginal)






