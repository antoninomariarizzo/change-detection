import numpy as np


def generate_data(n_pts: int = 1000,
                  low1: float = 0.0, high1: float = 1.0,
                  low2: float = -0.5, high2: float = 0.5):
    x = np.arange(n_pts)
    y = np.concatenate([np.random.uniform(low=low1, high=high1, size=n_pts // 2),
                        np.random.uniform(low=low2, high=high2, size=n_pts // 2)])
    cp_gt = n_pts // 2
    return x, y, cp_gt
