import numpy as np
import zarr
from . import store
from typing import Tuple, List


def select(SRC, LP, CH, REP) -> Tuple[List[zarr.Group], List[zarr.Group]]:
    ''' simple data selection '''
    droot = store.open_group()

    if np.isscalar(SRC):
        SRC = [SRC]
    if np.isscalar(LP):
        LP = [LP]
    if np.isscalar(CH):
        CH = [CH]
    if np.isscalar(REP):
        REP = [REP]

    targets = []
    for src in SRC:
        for lp in LP:
            for ch in CH:
                for rep in REP:
                    _validate_args(src, lp, ch, rep)
                    targets.append((src, lp, ch, rep))

    dat_grps = []
    sup_grps = []

    for t in targets:
        dat_grps.append(droot[_datapath(*t)])
        try:
            sup_grps.append(droot[_supdatapath(*t)])
        except KeyError:  # supdata is not available
            sup_grps.append(None)

    return dat_grps, sup_grps


def _validate_args(src, lp, ch, rep):
    assert src in [1, 2], f'message source index is either 1 or 2, get {src}'
    assert lp in range(-5, 4), f'launched power is from -5 to 3 (dBm), get {lp}'
    assert ch in range(1, 8), f'channel index is from 1 to 7, get {ch}'
    assert rep in [1, 2, 3], f'repeats index is from 1 to 3, get {rep}'


def _datapath(src, lp, ch, rep):
    return '1125km_SSMF/src%d/%ddBm_ch%d_%d' % (src, lp, ch, rep)


def _supdatapath(src, lp, ch, rep):
    return 'supdata/src%d/%ddBm_ch%d_%d' % (src, lp, ch, rep)

