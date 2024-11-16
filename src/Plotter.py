from typing import Union, List
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Union, Tuple


class Plotter:
    def __init__(self,
                 figsize: Tuple[int, int] = (12, 6),
                 dpi: int = 700,
                 base_path: str = None,
                 format: str = 'pdf'):
        self.figsize = figsize
        self.dpi = dpi
        self.base_path = base_path
        self.format = format

    def plot(self,
             x: np.ndarray,
             y: np.ndarray,
             stats: Union[List[float], np.ndarray] = None,
             thr: float = None,
             cp: int = None,
             cp_gt: int = None,
             title: str = None,
             figsize: Tuple[int, int] = None,
             fname: str = None) -> None:
        sns.set(style="darkgrid")

        if figsize is None:
            figsize = self.figsize

        if stats is None:
            plt.figure(figsize=figsize, dpi=self.dpi)
            sns.lineplot(x=x, y=y, color='k', label='Data')
            if cp_gt is not None:
                plt.axvline(x=cp_gt, color='green', linestyle='-', linewidth=3,
                            label='Change Point GT')
        else:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, dpi=self.dpi)

            sns.lineplot(x=x, y=y, ax=ax1, color='k', label='Data', legend=False)

            sns.lineplot(x=np.arange(len(stats)),
                         y=stats,
                         ax=ax2,
                         color='darkblue',
                         label='Stats',
                         legend=False)

            if thr is not None:
                ax2.axhline(y=thr, color='orange',
                            linestyle='--', label='Threshold')

            if cp_gt is not None:
                ax1.axvline(x=cp_gt, color='green', linestyle='-', linewidth=3,
                            label='Change Point GT')
                ax2.axvline(x=cp_gt, color='green', linestyle='-', linewidth=3,
                            label='Change Point GT')

            if cp is not None:
                ax1.axvline(x=cp, color='red', linestyle='-.',
                            label='Change Point')
                ax2.axvline(x=cp, color='red', linestyle='-.',
                            label='Change Point')

            if title is not None:
                plt.suptitle(title, fontsize=16, fontweight='bold', y=0.95)

            ax1.set_title('Input data', fontsize=14)
            ax2.set_title('Statistics', fontsize=14)

            handles1, labels1 = ax1.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()

            handles, labels = [], []
            for h, l in zip(handles1 + handles2, labels1 + labels2):
                if l not in labels:
                    handles.append(h)
                    labels.append(l)

            fig.legend(handles, labels, loc='lower center',
                       bbox_to_anchor=(0.5, -0.001), ncol=5)

            plt.tight_layout(rect=[0, 0.08, 1, 1])  # [0, 0, 1, 1]

        if fname is None:
            plt.show()
        else:
            plt.savefig(self.base_path + fname + '.' + self.format,
                        format=self.format,
                        dpi=self.dpi)
            plt.close()

    def compare_stats(self,
                      stats_py: Union[List[float], np.ndarray],
                      stats_r: Union[List[float], np.ndarray],
                      min_obs: int,
                      label1: str = 'Ours',
                      label2: str = 'R',
                      title: str = None,
                      fname: str = None) -> None:
        
        # Align our and R statistics
        stats_py = stats_py[min_obs+1:]
        stats_r = stats_r[min_obs:-min_obs-1]

        sum_abs_diff = np.sum(np.abs(stats_py - stats_r))
        print(f"Difference Ours and R versions: {sum_abs_diff}")

        plt.figure(figsize=self.figsize)
        sns.lineplot(x=np.arange(len(stats_py)),
                     y=stats_py,
                     color='darkblue', linewidth=4,
                     label=label1)
        sns.lineplot(x=np.arange(len(stats_r)),
                     y=stats_r,
                     color='darkorange',
                     label=label2)

        if title is not None:
            plt.suptitle(title, fontsize=16, fontweight='bold', y=0.95)

        plt.legend(loc='lower center',
                   bbox_to_anchor=(0.5, -0.5), ncol=5)

        plt.tight_layout(rect=[0, 0.25, 1, 1])  # [0, 0, 1, 1]

        if self.base_path is None or fname is None:
            plt.show()
        else:
            plt.savefig(self.base_path + fname + '.' + self.format,
                        format=self.format,
                        dpi=self.dpi)
            plt.close()
