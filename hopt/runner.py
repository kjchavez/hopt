from __future__ import print_function

import os
import sys
import time
import uuid

from google.protobuf import text_format
from hopt.experiment import Experiment
from hopt.trial import TrialData, new_trial, existing_trial
from hopt.experiment_pb2 import ExperimentDef


def format_results(params, upper_bound, trial_id=""):
    out = "="*80 + '\n'
    out += "Trial %s\n" % trial_id
    out += "="*80 + '\n'
    out += "Params:\n"
    for p, v in params.items():
        out += "%s = %s\n" % (p, str(v))
    out += "\nUpper bound on value = %s\n" % (str(upper_bound),)
    return out


def run_once(experiment):
    trial = new_trial(experiment)
    with trial:
        # Run the evaluation function.
        score = experiment.evaluate_fn(trial.params, trial.trial_dir,
                                       time_limit=None)
        trial.update_score(score)

    print(format_results(trial.params, trial.score, trial_id=trial.trial_dir))

def run_n_trials(experiment_def, N):
    """ Loads ExperimentDef and runs N trials sequentially. """
    with open(experiment_def) as fp:
        experiment_def = text_format.Parse(fp.read(), ExperimentDef())

    experiment = Experiment(experiment_def)
    for _ in xrange(N):
        run_once(experiment)

def resume_trial(experiment_def, trial_dir):
    trial = existing_trial(trial_dir)
    with open(experiment_def) as fp:
        experiment_def = text_format.Parse(fp.read(), ExperimentDef())

    experiment = Experiment(experiment_def)
    with trial:
        score = experiment.evaluate_fn(trial.params, trial.trial_dir,
                                       time_limit=None)
        trial.update_score(score)

    print(format_results(trial.params, trial.score, trial_id=trial.trial_dir))

