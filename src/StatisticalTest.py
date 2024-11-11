import numpy as np
from scipy.stats import mannwhitneyu, mood
from abc import ABC, abstractmethod
from typing import List, Union
import inspect


class Test(ABC):
    @abstractmethod
    def statistic(self,
                  seq1: Union[List[float], np.ndarray],
                  seq2: Union[List[float], np.ndarray]) -> float:
        """
        Compute the test statistic.

        Parameters:
            seq1 (List[float] or np.ndarray): First data sequence.
            seq2 (List[float] or np.ndarray): Second data sequence.
            alternative (str): Defines the alternative hypothesis ('two-sided', 'less', or 'greater').

        Returns:
            stat(float): test statistic.
        """
        fun_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError(f"Must override {fun_name} method")


class MannWhitneyU(Test):
    @staticmethod
    def statistic(seq1: Union[List[float], np.ndarray],
                  seq2: Union[List[float], np.ndarray],
                  alternative: str = 'two-sided') -> float:
        """
        Calculate the z-score for the Mann-Whitney U statistic, normalized by sample size.
        Detect location (mean) shifts in a stream with a (possibly unknown) non-Gaussian distribution.

        Parameters:
            seq1 (List[float] or np.ndarray): First data sequence.
            seq2 (List[float] or np.ndarray): Second data sequence.
            alternative (str): Defines the alternative hypothesis ('two-sided', 'less', or 'greater').

        Returns:
            stat(float): Z-score of the Mann-Whitney U statistic.
        """

        len1 = len(seq1)
        len2 = len(seq2)
        len12 = len1 + len2

        # Mann-Whitney U statistic using scipy
        U, _ = mannwhitneyu(seq1, seq2, alternative=alternative)

        # Compute the mean and standard deviation under the null hypothesis
        mu_U = len1 * len2 / 2
        sigma_U = np.sqrt(len1 * len2 * (len12 + 1) / 12)

        # Compute the z-score
        stat = (U - mu_U) / sigma_U
        return abs(stat)

    def __str__(self):
        return "MannWhitneyU"


class Mood(Test):
    @staticmethod
    def statistic(seq1: Union[List[float], np.ndarray],
                  seq2: Union[List[float], np.ndarray]) -> float:
        """
        Compute the Mood test statistic for two sequences.
        Detect scale (variance) shifts in a stream with a (possibly unknown) non-Gaussian distribution.

        Parameters:
            seq1 (List[float] or np.ndarray): First data sequence.
            seq2 (List[float] or np.ndarray): Second data sequence.

        Returns:
            stat(float): Mood's test statistic.
        """
        stat, _ = mood(seq1, seq2)
        return abs(stat)

    def __str__(self):
        return "Mood"


class Lepage(Test):
    @staticmethod
    def statistic(seq1: Union[List[float], np.ndarray],
                  seq2: Union[List[float], np.ndarray]) -> float:
        """
        Compute the Lepage test statistic for two series.
        The Lepage statistic is the squared sum of squared Mann-Whitney 
        and Mood's test statistics.
        Detect location and scale shifts in a stream with a (possibly unknown) non-Gaussian distribution.

        Parameters:
            seq1 (List[float] or np.ndarray): First data sequence.
            seq2 (List[float] or np.ndarray): Second data sequence.

        Returns:
            stat(float): Lepage test statistic.
        """

        # Compute Mann-Whitney U statistic for location differences
        mannwhitney_stat = MannWhitneyU.statistic(seq1, seq2,
                                                   alternative='two-sided')

        # Compute Mood's test statistic for dispersion differences
        mood_stat = Mood.statistic(seq1, seq2)

        # Combine MannWhitneyU and Mood statistics
        stat = mannwhitney_stat**2 + mood_stat**2
        return stat

    def __str__(self):
        return "Lepage"
