from typing import List
from trueskill.engine.true_skill_two_player import update_rating
from trueskill.engine.true_skill_two_teams import update_ratings_in_team
from trueskill.engine.true_skill import TrueSkillEnv
from trueskill.utils.constants import DYNAMIC_FACTOR, PERFORMANCE_NOISE
from trueskill.data.player_ratings import CsvSource
from trueskill.data.game import load_teams_from_game_info


def calculate_skill(game_info: str, ranks: List[int], save_dir='.',
                    dynamic=DYNAMIC_FACTOR, perf_noise=PERFORMANCE_NOISE):
    """Update the skills of 1+ players in 2+ teams.

    Args:
        game_info: Filepath to CSV containing game outcome information. CSV
        format is every row is a team and individual values in a row are
        players in that team.
        ranks: Where each team ranked in the game, with low being the best.
        save_dir: Directory in which the CSV database is found. Defaults to
        current directory.
        dynamic: Factor allowing skill to vary over time.
        perf_noise: Standard deviation of performance noise.
    Returns:
        None
    Raises:
        ValueError: If there is something wrong with input data
    """
    # data validation
    teams = load_teams_from_game_info(game_info)
    if len(teams) != len(ranks):
        raise ValueError("Rank must be given for each team.")
    if len(ranks) != len(set(ranks)):
        raise ValueError("Ranks must be unique.")

    # connect to the data source and populate data structure for team skills
    data_src = CsvSource(save_dir)
    teams = [i for _, i in sorted(zip(ranks, teams))]
    all_team_skills = []
    for team in teams:
        team_skills = {}
        for player in team:
            player_skill = data_src.load_player_ratings(player)
            team_skills[player] = player_skill
        all_team_skills.append(team_skills)

    # start the engine environment and bulk update the ratings
    ts_env = TrueSkillEnv(all_team_skills, dynamics=dynamic,
                          perf_noise_sigma=perf_noise)
    new_ratings = ts_env.update_ratings()
    data_src.bulk_update_player_ratings(new_ratings)


# TODO: Remove these two methods as they are now made redundant by the above.
def calculate_skill_1vs1(player_one: str, player_two: str, save_dir='.'):
    """ This method is now superseded by the general "calculate_skill()".
    Calculate the new skills of two players in a 1vs1 match where the first
    is assumed to be the winner and the second the loser of the match. If the
    players are found in the data source their skills are updated accordingly
    if not new entries are made for the players. It is assumed players have
    unique usernames.

    Args:
        player_one: The username of the first player, the winner.
        player_two: The username of the second player, the loser.
        save_dir: The directory where the skills CSV file is located.
    """
    # connect to the data source
    data_source = CsvSource(data_dir=save_dir)

    # update ratings given match outcome - calculate posterior
    p1_skill = data_source.load_player_ratings(player_one)
    p2_skill = data_source.load_player_ratings(player_two)
    p1_rating, p2_rating = update_rating(p1_skill, p2_skill)

    # save the new ratings
    data_source.update_player_rating(player_one, p1_rating)
    data_source.update_player_rating(player_two, p2_rating)
    data_source.save_player_ratings(data_dir=save_dir)


def calculate_skills_1teamvs1team(winning_team: List[str],
                                  losing_team: List[str],
                                  save_dir='.'):
    """
    Legacy method for calculating TrueSkill updates for two team game.
    Args:
        winning_team: A list of player names on the winning team
        losing_team: A list of player names on the losing team
        save_dir: the directoru where the skills CSV file is located
    Raises:
        ValueError: If there is something wrong with the player names in the
        teams.
    """
    if len(winning_team) != len(set(winning_team)):
        raise ValueError("Unique player names required in winning team.")
    if len(losing_team) != len(set(losing_team)):
        raise ValueError("Unique player names required in losing team.")
    if len(set(winning_team).intersection(set(losing_team))) > 0:
        raise ValueError("There can't be the same player in both teams.")
    # connect to the data source
    data_src = CsvSource(data_dir=save_dir)

    # update ratings given match outcome
    winning_ratings = {p:data_src.load_player_ratings(p) for p in winning_team}
    losing_ratings = {p:data_src.load_player_ratings(p) for p in losing_team}
    update_ratings_in_team(winning_ratings, losing_ratings)

    # save the updated ratings
    all_ratings = winning_ratings.update(losing_ratings)
    data_src.bulk_update_player_ratings(all_ratings)
    data_src.save_player_ratings(data_dir=save_dir)



