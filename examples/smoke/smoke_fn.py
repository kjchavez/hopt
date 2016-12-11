def main(params, time_limit=None):
    if 'x' not in params or 'y' not in params:
        # Invalid set of params
        return None

    return params['x']*params['y']
