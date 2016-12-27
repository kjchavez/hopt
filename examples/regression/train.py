import tensorflow as tf
from tensorflow.contrib.framework.python.ops import variables
import os

import numpy as np

# Let's create a very simple logistic regression model with regularization.

INPUT_DIM = 2
BATCH_SIZE = 100
def model_fn(X, target, mode, params):
    reg = params['reg']
    lr = params['lr']
    W = variables.model_variable('W', shape=(INPUT_DIM,),
                                 initializer=tf.random_normal_initializer(
                                                mean=0.0,
                                                stddev=0.001))

    b = variables.model_variable('b', shape = (1,),
                                 initializer=tf.constant_initializer(0.0))
    Y = W*X
    print "Y shape:", Y.get_shape()

    logit = tf.reduce_sum(Y, 1) + b
    print "logit: shape", logit.get_shape()
    # y = tf.sigmoid(logit)
    pred = logit > 0

    if mode is tf.contrib.learn.ModeKeys.TRAIN:
        loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logit,
                                                                      target),
                              0)
        loss += reg * tf.nn.l2_loss(W)
        optimizer = tf.train.GradientDescentOptimizer(lr)
        global_step = variables.get_global_step()
        train_op = optimizer.minimize(loss, global_step=global_step)
    else:
        loss, train_op = None, None

    return (pred, loss, train_op)


# Generate synthetic data.
STDDEV = np.sqrt(32)
SYN_Y = np.random.choice([0, 1], size=(1000,)).astype(np.float32)
COPT = np.array([[4, 4], [-4,-4]]).astype(np.float32)
C = COPT[SYN_Y.astype(np.uint8)]
SYN_X = STDDEV*np.random.randn(1000, INPUT_DIM).astype(np.float32) + C
DATA = np.concatenate((SYN_X, np.reshape(SYN_Y, (-1, 1))), 1)

def get_data(begin, end):
    data = tf.train.input_producer(DATA[begin:end])
    data = data.dequeue_many(BATCH_SIZE)
    X = data[:, 0:2]
    y = data[:, 2]
    return X, y

def get_train_data():
    return get_data(0, 800)

def get_val_data():
    return get_data(800, 1000)

def main(params, trial_dir, time_limit=None):
    # Instead of using the tf logging for information:
    #   tf.logging.set_verbosity(tf.logging.INFO)
    # we will explicitly record information of interest. Still need to figure
    # out how to redirect all of TF output to those stdout, stderr files we
    # create in the trial directory.

    model_dir = os.path.join(trial_dir, "model")
    print("Saving to %s" % model_dir)
    config = tf.contrib.learn.RunConfig(save_checkpoints_secs=10)
    estimator = tf.contrib.learn.Estimator(model_fn=model_fn,
                                                   model_dir=model_dir,
                                                   config=config,
                                                   params=params)
    estimator.fit(input_fn=get_train_data, steps=1000)
    predictions = estimator.predict(x=SYN_X[800:1000], as_iterable=True)
    num_correct = 0
    for i, p in enumerate(predictions):
        print("%s / %s" % (p, bool(SYN_Y[800+i])))
        num_correct += (p == SYN_Y[800+i])

    accuracy = float(num_correct) / 200
    print("Accuracy = %0.4f" % accuracy)
    return accuracy

if __name__ == "__main__":
    main({'reg': 0.000, 'lr': 0.001}, "trial-dir")
