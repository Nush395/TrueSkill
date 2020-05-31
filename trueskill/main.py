from trueskill.utils.calculate_ratings import calculate_skill
from trueskill.utils.constants import DYNAMIC_FACTOR, PERFORMANCE_NOISE
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--ranks", type=int,  nargs='+',
                        help="Team rankings.", required=True)
    parser.add_argument("-g", "--game-info", type=str, required=True,
                        help="Path to game info CSV file. Rows in the CSV "
                             "represent teams,  and values in the row will be"
                             " interpreted as the player identifiers.")
    parser.add_argument("-d", "--save-dir", type=str, required=False,
                        help="Path to the directory where true skill ratings"
                             "for players are saved in the true_skills.csv "
                             "file. If this file does not already exist it "
                             "will be created with new player ratings. "
                             "Defaults to the current directory.",
                        default='.')
    parser.add_argument("--dynamic", type=float, required=False,
                        default=DYNAMIC_FACTOR,
                        help="Dynamic factor that allows the prior skill to"
                             "vary over time.")
    parser.add_argument("--perf-noise", type=float, required=False,
                        default=PERFORMANCE_NOISE,
                        help="Standard deviation of the performance noise.")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    calculate_skill(args.game_info, args.ranks, save_dir=args.save_dir,
                    dynamic=args.dynamic,  perf_noise=args.perf_noise)



