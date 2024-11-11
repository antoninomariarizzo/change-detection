import numpy as np
from pyper import R   # pip install PypeR


def cpm_r(data: np.ndarray,
          test: str,
          alpha: float = 0.005,
          min_obs: int = 8) -> np.ndarray:

    rr = R()
    rr('library("cpm")')
    rr.change_point_min_samples = min_obs

    r_cmds = [
        'cc<-as.numeric(unlist(lik))',
        'cp<-detectChangePointBatch(cc,"{}", alpha={}, lambda=NA)'.format(test, alpha),
        'a<-cp',
    ]
    rr.lik = data.astype(str)
    rr(r_cmds)
    return rr.a['Ds']
