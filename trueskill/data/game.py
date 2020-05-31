from typing import List
import os


def load_teams_from_game_info(game_info: str):
    """Load and validate players and teams from a CSV file.

    Args:
        game_info: Path to the game outcome information file.

    Returns:

    """
    if not os.path.exists(game_info):
        raise FileExistsError("Invalid path to game info CSV file.")
    teams = []
    with open(game_info, "r") as f:
        line = f.readline().strip("\n")
        while line:
            players = line.split(",")
            teams.append(players)
            line = f.readline().strip("\n")
    validate_teams(teams)
    return teams


def validate_teams(teams: List[List[str]]):
    """Validates team information.

    Args:
        teams: A list of lists, where each sublist contains players in the team
    Raises:
        ValueError: If the team information is not consistent.
    """
    if not len(teams) >= 2:
        raise ValueError("Need at least two players in the game!")
    players_seen = set()
    for team in teams:
        for player in team:
            if player not in players_seen:
                players_seen.add(player)
            else:
                raise ValueError(f"Player {player} present multiple times.")


