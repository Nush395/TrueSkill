import unittest
from src.trueskill.constants import MU, SIGMA
from src.data.data import CsvSource
from src.utils.maths import Gaussian


class TestCsvSource(unittest.TestCase):
    def setUp(self) -> None:
        self.source = CsvSource()

    def test_load_player_ratings_for_new_player(self):
        # given
        new_player = 'hello TrueSkill'

        # when
        self.source.load_player_ratings(new_player)

        # then
        expected_rating = Gaussian(mu=MU, sigma=SIGMA)
        self.assertEqual(self.source.data[new_player], expected_rating)

    def test_load_player_ratings_for_existing_player(self):
        # given
        existing_player = 'A True Skill Veteran'
        existing_rating = Gaussian(mu=1, sigma=1)
        self.source.data[existing_player] = existing_rating

        # when
        self.source.load_player_ratings(existing_player)

        # then
        self.assertEqual(self.source.data[existing_player], existing_rating)

    def test_update_player_rating(self):
        # given
        player = 'foo'
        rating = Gaussian(mu=1, sigma=1)
        self.source.data[player] = Gaussian(mu=0, sigma=10)

        # when
        self.source.update_player_rating(player, rating)

        # then
        self.assertEqual(self.source.data[player], rating)