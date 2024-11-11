from abc import ABC, abstractmethod
import numpy as np
import inspect
from typing import List, Union, Tuple


class ChangeDetector(ABC):
    def __init__(self,
                 thr: float):
        self.thr = thr
        self.change_detected = False

    @abstractmethod
    def detect_changes(self, 
                       data: Union[List[float], np.ndarray]) -> Tuple[List[int], List[float]]:
        """
        Detect change points in a data stream.
        Return the change points and the test statistics.
        """
        fun_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError(f"Must override {fun_name} method")
