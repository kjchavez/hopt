from .context import hopt
import os
import google.protobuf.text_format as text_format

def get_experiment():
    experiment_prototxt = """
    experiment_name: "smoke"
    path: "examples"
    module: "smoke.smoke_fn"
    output_path: "/tmp/hopt/test"
    variable {
      name: "x"
      type: FLOAT
      sample_strategy {
        distribution: LOG_UNIFORM
        minimum: 1e-6
        maximum: 1e-1
      }
    }
    variable {
      name: "y"
      type: INTEGER
      sample_strategy {
        distribution: UNIFORM
        minimum: 0
        maximum: 10
      }
    }
    """
    exp_def = text_format.Parse(experiment_prototxt,
                                hopt.ExperimentDef())
    return hopt.Experiment(exp_def)

def test_new_trial_stdout_redirect():
    experiment = get_experiment()
    trial = hopt.new_trial(experiment)
    with trial:
        print "This should go to a file."

    with open(trial.stdout_filename) as fp:
        assert next(fp).strip() == "This should go to a file."

    os.remove(trial.stdout_filename)
