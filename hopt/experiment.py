import numpy as np
import random
from hopt.experiment_pb2 import *

def _float_uniform_sample(minimum, maximum):
    return np.random.uniform(minimum, maximum)

def _float_log_uniform_sample(minimum, maximum):
    log_min = np.log(minimum)
    log_max = np.log(maximum)
    log_sample = np.random.uniform(log_min, log_max)
    return np.exp(log_sample)

def _int_uniform_sample(minimum, maximum):
    return np.random.randint(minimum, maximum)

def _int_log_uniform_sample(minimum, maximum):
    log_min = np.log(minimum)
    log_max = np.log(maximum)
    log_sample = np.random.uniform(log_min, log_max)
    return int(np.round(np.exp(log_sample)))

def _enum_uniform_sample(values):
    return random.choice(values)

def get_sample_function(var_type, sample_strategy):
    """ Returns the appropriate sampling function for a given variable type and
    sampling strategy.
    """
    fn = {}
    fn[(Variable.FLOAT, SampleStrategy.UNIFORM)] = _float_uniform_sample
    fn[(Variable.FLOAT, SampleStrategy.LOG_UNIFORM)] = _float_log_uniform_sample
    fn[(Variable.INTEGER, SampleStrategy.UNIFORM)] = _int_uniform_sample
    fn[(Variable.INTEGER, SampleStrategy.LOG_UNIFORM)] = _int_log_uniform_sample
    fn[(Variable.ENUM, SampleStrategy.UNIFORM)] = _enum_uniform_sample

    key = (var_type, sample_strategy.distribution)
    if key not in fn:
        raise TypeError("No sampling function available for %s, %s" %
                        (var_type, sample_strategy.distribution))

    return lambda: fn[key](sample_strategy.minimum, sample_strategy.maximum)


class ParameterSampler(object):
    def __init__(self, variable_def):
        self.variable_name = variable_def.name
        self.variable_type = variable_def.type
        self.sample_fn = get_sample_function(self.variable_type,
                                             variable_def.sample_strategy)
        self.history = []

    def sample(self):
        """ Returns a tuple of variable name and value. """
        sample = self.sample_fn()
        self.history.append(sample)
        return (self.variable_name, sample)


class Experiment(object):
    def __init__(self, experiment_def):
        self.name = experiment_def.experiment_name
        self.samplers = [ParameterSampler(var_def) for var_def in
                         experiment_def.variable]

    def sample_parameters(self):
        return dict(sampler.sample() for sampler in self.samplers)
