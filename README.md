# hopt

Simple harness for hyperparameter optimization. Primarily for TensorFlow models.

## V0 Requirements

* Support specifying the search space and sampling strategy. (DONE)
* Create well-structured output directories. (DONE)
* Allow *continuing* or *refining* a simple experiment instance manually.
* Command line utility for all of this.


### Overview

This framework does a simple random search for a good set of hyperparameters.
The user specifies:

- An ExperimentDef proto which defines the search space and
  sampling strategy for the parameters.
- A function that takes the parameters and a time limit and returns an upper
  bound on the value of that set of parameters.

Some questions.

1. Should the function be a python function that we can 'import' and 'invoke'
   or can it simply be anything that can be invoked from the command line?
   If the latter, how do we get the 'return' value?

