import argparse

import hopt

def run(args):
    """ Handle the 'run' subcommand. """
    hopt.run_n_trials(args.experiment_def, args.num_trials)


def parse_args():
    parser = argparse.ArgumentParser("Tool for finding hyperparameters.")
    subparsers = parser.add_subparsers(help="Subcommands")

    # First subcommand.
    run_parser = subparsers.add_parser('run', help="Start running an experiment.")
    run_parser.add_argument("experiment_def", type=str,
                            help="ExperimentDef in proto text.")
    run_parser.add_argument("--num-trials", '-n', type=int,
                            help="Number of trials to execute.")
    run_parser.set_defaults(func=run)

    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
