import unittest
from trueskill.true_skill_two_player import update_rating
from trueskill.true_skill_two_teams import update_ratings_in_team
from trueskill.true_skill import TrueSkill
from trueskill import MU, SIGMA
from maths import Gaussian


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
        ts = TrueSkill(teams)
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
        ts = TrueSkill(teams)
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
        ts = TrueSkill(teams)
        ts.update_ratings()

        # then expect a convergence



