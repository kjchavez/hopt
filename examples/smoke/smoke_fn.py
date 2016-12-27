def main(params, trial_dir, time_limit=None):
    if 'x' not in params or 'y' not in params:
        # Invalid set of params
        return None
    print "This should show up in the stdout file."
    print "And this."

    return params['x']*params['y']
