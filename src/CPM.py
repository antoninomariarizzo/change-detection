import numpy as np
from src.ChangeDetector import ChangeDetector
from src import StatisticalTest
from typing import List, Union, Tuple


class CPM(ChangeDetector):
    def __init__(self,
                 test: StatisticalTest,
                 thr: float = 19.6325,
                 min_obs: int = 8):
        self.test = test
        self.thr = thr
        self.min_obs = min_obs
        self.change_detected = False

    def detect_changes(self, 
                       data: Union[List[float], np.ndarray]) -> Tuple[List[int], List[float]]:
        """
        Detect change points in a data stream.

        Parameters:
        - data (Union[List[float], np.ndarray]): Data to monitor.

        Returns:
        - change points (List[int]): indices where changes are detected
        - stats(List[float]): test statistics computed at each step
        """
        n_pts = len(data)
        change_points = []
        stats = [0.] * (self.min_obs - 1)

        # Evaluate each possible change point
        for cp in range(self.min_obs, n_pts - self.min_obs):
            # For each candidate change point, split the data into two sequences
            seq1, seq2 = data[:cp], data[cp:]

            # Compute test statistic for the split
            stat = self.test.statistic(seq1, seq2)
            stats.append(stat)

        # Compute the maximum test statistic
        stat_max = max(stats)

        # Detect the change point when the stat_max exceeds a threshold
        if stat_max > self.thr:
            self.change_detected = True
            cp = stats.index(stat_max)
            change_points.append(cp)

        return change_points, stats
    
    def __str__(self):
        return f"CPM and {self.test()} test"
