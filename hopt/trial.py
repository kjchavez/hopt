from __future__ import print_function

import numpy as np
import os
import sys
import time
import uuid
import yaml


def get_timestamp():
    return time.strftime("%d %b %Y %H:%M:%S")


"""
Sample Usage:

Ex 1.
    with new_trial(experiment, params) as trial:
        value = experiment.evaluate_fn(params, time_limit=None)
        trial.update_score(value)

Ex 2.
    with existing_trial(trial_dir) as trial:
        value = experiment.evaluate_fn(params, time_limit=None)
        trial.update_score(value)
"""
class TrialData(object):
    def __init__(self, trial_dir, params=None, experiment=None):
        self.trial_dir = trial_dir
        if experiment:
            self.experiment = experiment

        # Important filenames
        self.metadata_filename = os.path.join(trial_dir, 'METADATA')
        self.results_filename = os.path.join(trial_dir, 'results.txt')
        self.stdout_filename = os.path.join(trial_dir, 'stdout.txt')

        self.score = self._load_score()
        if os.path.exists(self.metadata_filename):
            assert params is None
            self.params =self. _load_params()
        else:
            self.params = params
            self._write_metadata()

    def _load_params(self):
        assert os.path.exists(self.metadata_filename)
        with open(self.metadata_filename) as fp:
            metadata = yaml.load(fp)

        return metadata['parameters']

    def _load_score(self):
        """ Returns a score from the results file or -inf if None is found."""
        if not os.path.exists(self.results_filename):
            return -np.inf

        with open(self.results_filename, 'r') as fp:
            scores = [float(line.split(',')[0]) for line in fp]

        if len(scores) == 0:
            return -np.inf
        else:
            return max(scores)

    def _write_metadata(self):
        metadata = {}
        metadata['start_timestamp'] = get_timestamp()
        metadata['parameters'] = self.params
        metadata['experiment_def_path'] = self.experiment_def_path
        with open(self.metadata_filename, 'w') as fp:
            yaml.dump(metadata, fp)

    def __enter__(self):
        self.prev_stdout = sys.stdout
        sys.stdout = open(self.stdout_filename, 'a')

    def __exit__(self, type, value, traceback):
        sys.stdout = self.prev_stdout

    def update_score(self, new_score):
        if new_score > self.score:
            self.score = new_score

        with open(self.results_filename, 'a') as fp:
            print('%f, %s' % (new_score, get_timestamp()), file=fp)

    def get_experiment(self):
        """ Reconstructs (if necessary) and returns parent experiment. """

def new_trial(experiment):
    dirname = 'trial-' + str(uuid.uuid4()).split('-')[-1]
    dirname = os.path.join(experiment.output_dir, dirname)
    os.mkdir(dirname)
    params = experiment.sample_parameters()
    return TrialData(dirname, params=params)

def existing_trial(trial_dir):
    return TrialData(trial_dir, params=None)
