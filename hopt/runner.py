from hopt.experiment import Experiment
from hopt.experiment_pb2 import ExperimentDef

import argparse
from google.protobuf import text_format


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_def", type=str,
                        help="Proto text file defining experiment")
    return parser.parse_args()


def format_results(params, upper_bound, iteration=None):
    out = "="*80 + '\n'
    out += "Evaluation" + ("#%d\n" if iteration is not None else "\n")
    out += "="*80 + '\n'
    out += "Params:\n"
    for p, v in params.items():
        out += "%s = %s\n" % (p, str(v))
    out += "\nUpper bound on value = %s\n" % (str(upper_bound),)
    return out


def run_once(experiment):
    params = experiment.sample_parameters()
    value = experiment.evaluate_fn(params, time_limit=None)
    print format_results(params, value, iteration=1)


def main():
    args = parse_args()

    with open(args.experiment_def) as fp:
        experiment_def = text_format.Parse(fp.read(), ExperimentDef())

    experiment = Experiment(experiment_def)
    run_once(experiment)


if __name__ == "__main__":
    main()
