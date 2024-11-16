import numpy as np
from src.ChangeDetector import ChangeDetector
from typing import List, Union, Tuple


class pyCUSUM(ChangeDetector):
    def __init__(self,
                 thr: float = 9.,
                 margin: float = 0.1,
                 min_obs: int = 8):
        self.n_pts = 0
        self.running_mean = 0.0
        self.sum_high = 0.0
        self.sum_low = 0.0
        self.margin = margin
        self.thr = thr
        self.min_obs = min_obs
        self.change_detected = False

    def update(self, value: float) -> None:    
        """
        Update the test statistic based on a new observation value.

        Parameters:
        - value (float): The new data point to process.
        """
        self.n_pts += 1
        self.running_mean += (value - self.running_mean) / self.n_pts
        self.sum_high = max(0, self.sum_high + value - self.running_mean - self.margin)
        self.sum_low = max(0, self.sum_low - value + self.running_mean - self.margin)
        
        if self.n_pts < self.min_obs:
            return

        if self.sum_high > self.thr or self.sum_low > self.thr:
            self.change_detected = True

    def reset(self) -> None:
        """
        Reset the internal state to the initial values.
        """
        self.n_pts = 0
        self.running_mean = 0.0
        self.sum_high = 0.0
        self.sum_low = 0.0
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
        change_points = []
        stats = []

        # Monitor incoming samples as they arrive (sequential monitoring)
        for i, val in enumerate(data):
            self.update(val)
            stats.append(max(self.sum_high, self.sum_low))

            if self.change_detected:
                change_points.append(i)
                self.reset()

        return change_points, stats

    def __str__(self):
        return "CUSUM"
