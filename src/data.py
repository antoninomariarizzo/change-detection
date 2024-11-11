import numpy as np


def generate_data(n_pts: int = 1000):
    x = np.arange(n_pts)
    y = np.concatenate([np.random.uniform(low=0, high=1, size=n_pts // 2),
                        np.random.uniform(low=-.5, high=.5, size=n_pts // 2)])
    cp_gt = n_pts // 2
    return x, y, cp_gt
