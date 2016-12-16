import argparse

import hopt

def run(args):
    hopt.run_n_trials(args.experiment_def, args.num_trials)


def resume(args):
    hopt.resume_trial(args.experiment_def, args.trial_dir)


def parse_args():
    parser = argparse.ArgumentParser("Tool for finding hyperparameters.")
    subparsers = parser.add_subparsers(help="Subcommands")

    # 'run' subcommand.
    run_parser = subparsers.add_parser('run', help="Start running an experiment.")
    run_parser.add_argument("experiment_def", type=str,
                            help="ExperimentDef in proto text.")
    run_parser.add_argument("--num-trials", '-n', type=int,
                            default=10,
                            help="Number of trials to execute.")
    run_parser.set_defaults(func=run)

    # 'resume' subcommand
    resume_parser = subparsers.add_parser('resume',
                                          help="Resume an existing trial.")
    resume_parser.add_argument("experiment_def", type=str,
                               help="ExperimentDef in proto text.")
    resume_parser.add_argument("trial_dir", type=str,
                               help="Directory of trial to resume.")
    resume_parser.set_defaults(func=resume)

    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
