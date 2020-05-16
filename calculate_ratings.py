from true_skill_two_player import update_rating
from data import CsvSource


def calculate_skill_1vs1(player_one: str, player_two: str, save_dir='.'):
    """Calculate the new skills of two players where the first is assumed
     to be the winner and the second the loser of the match. If the players
     are found in the data source their skills are updated accordingly if not
     new entries are made for the players.
     Assumed players have unique usernames.

     Args:
         player_one: The username of the first player, the winner.
         player_two: The username of the second player, the loser.
         save_dir: The directory where the skills CSV file is located.
    """
    data_source = CsvSource(data_dir=save_dir)
    p1_skill = data_source.load_player_ratings(player_one)
    p2_skill = data_source.load_player_ratings(player_two)
    p1_rating, p2_rating = update_rating(p1_skill, p2_skill)
    data_source.update_player_rating(player_one, p1_rating)
    data_source.update_player_rating(player_two, p2_rating)
    data_source.save_player_ratings(data_dir=save_dir)


