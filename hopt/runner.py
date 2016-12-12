from __future__ import print_function

import argparse
import os
import sys
import time
import uuid

from google.protobuf import text_format
from hopt.experiment import Experiment
from hopt.experiment_pb2 import ExperimentDef


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_def", type=str,
                        help="Proto text file defining experiment")
    return parser.parse_args()


def get_timestamp():
    return time.strftime("%d %b %Y %H:%M:%S")


def format_results(params, upper_bound, trial_id=""):
    out = "="*80 + '\n'
    out += "Trial %s\n" % trial_id
    out += "="*80 + '\n'
    out += "Params:\n"
    for p, v in params.items():
        out += "%s = %s\n" % (p, str(v))
    out += "\nUpper bound on value = %s\n" % (str(upper_bound),)
    return out

def create_trial_directory(root, params):
    """ Creates a new directory for storing info about a trial.

    Arguments
        root: root output directory, must already exist
        experiment_name: name of the experiment which this trial belongs to
        params: dictionary of parameters used for this trial

    Returns:
        name of new directory
    """
    TRIAL_METADATA_FILENAME = 'METADATA'
    # Directory name is based on either: timestamp, counter, or uuid
    dirname = 'trial-' + str(uuid.uuid4()).split('-')[-1]
    full_name = os.path.join(root, dirname)
    os.mkdir(full_name)

    # Add a metadata file with parameters and creation timestamp
    with open(os.path.join(full_name, TRIAL_METADATA_FILENAME), 'w') as fp:
        print("Created at:", get_timestamp(), file=fp)
        print("\nParameters:", file=fp)
        print("-"*80, file=fp)
        for key, value in params.items():
            print("%s = %s" % (key, str(value)), file=fp)
        print("-"*80, file=fp)

    return dirname


def create_if_not_exists(path):
    assert (os.path.isdir(path) or not os.path.exists(path))
    if not os.path.exists(path):
        os.makedirs(path)


def run_once(experiment):
    params = experiment.sample_parameters()

    # Create a new directory for data from this trial.
    create_if_not_exists(experiment.output_dir)
    dirname = create_trial_directory(experiment.output_dir, params)

    # Redirect stdout to a text file.
    stdout_filename = os.path.join(os.path.join(experiment.output_dir, dirname),
                                   'stdout.txt')
    stdout = sys.stdout
    sys.stdout = open(stdout_filename, 'a')

    # Run the evaluation function.
    value = experiment.evaluate_fn(params, time_limit=None)

    # Update results file.
    results_filename = os.path.join(os.path.join(experiment.output_dir,
                                                 dirname),
                                    'results.txt')
    with open(results_filename, 'a') as fp:
        print('%f, %s' % (value, get_timestamp()), file=fp)

    # Restore stdout.
    sys.stdout = stdout
    print(format_results(params, value, trial_id=dirname))
    print("Output dir:", os.path.join(os.path.abspath(experiment.output_dir),
                                      dirname))
    print ("="*80)

def run_n_trials(experiment_def, N):
    """ Loads ExperimentDef and runs N trials sequentially. """
    with open(experiment_def) as fp:
        experiment_def = text_format.Parse(fp.read(), ExperimentDef())

    experiment = Experiment(experiment_def)
    for _ in xrange(N):
        run_once(experiment)

def main():
    args = parse_args()
    run_n_trials(args.experiment_def, 1)

if __name__ == "__main__":
    main()
