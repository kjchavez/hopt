from hopt.experiment import Experiment
from hopt.experiment_pb2 import ExperimentDef

import argparse
from google.protobuf import text_format
import importlib
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_def", type=str,
                        help="Proto text file defining experiment")
    return parser.parse_args()

def load_experiment_module(experiment_def):
    module = experiment_def.module
    package = experiment_def.pkg
    if len(package) == 0:
        package = None

    if experiment_def.path:
        sys.path.insert(0, os.path.abspath(experiment_def.path))

    return importlib.import_module(module, package=package)

def main():
    args = parse_args()

    with open(args.experiment_def) as fp:
        experiment_def = text_format.Parse(fp.read(), ExperimentDef())

    experiment = Experiment(experiment_def)
    exp_module = load_experiment_module(experiment_def)

    # Module must expose a top level function called 'main'
    evaluate_fn = exp_module.main
    params = experiment.sample_parameters()
    value = evaluate_fn(params, time_limit=None)
    print
    print "="*80
    print "Evaluation #1"
    print "="*80
    print "Params:"
    for p, v in params.items():
        print "%s = %s" % (p, str(v))
    print
    print "Upper bound on value =", value

if __name__ == "__main__":
    main()
