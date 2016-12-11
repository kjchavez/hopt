from .context import hopt
import google.protobuf.text_format as text_format

experiment_prototxt = """
experiment_name: "smoke"
path: "examples"
module: "smoke.smoke_fn"
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

def test_sample_parameters():
    exp_def = text_format.Parse(experiment_prototxt,
                                hopt.ExperimentDef())
    exp = hopt.Experiment(exp_def)
    params = exp.sample_parameters()
    print params
    assert len(params.keys()) == 2
    assert 'x' in params
    assert 'y' in params
    assert 1e-6 <= params['x'] <= 1e-1
    assert 0 <= params['y'] <= 10
