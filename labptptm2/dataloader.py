import os
import io
import h5py
import dvc.api
import contextlib
import numpy as np
from pathlib import Path
from tqdm import tqdm

_conf = {'repo': 'https://github.com/remifan/LabPtPTm2',
         'supdata': False,
         'local': True,
         'dump': True,
         'dump_dir': os.path.join(os.getcwd(), 'labptptm2_data')}


def config(**kwargs):
    _conf.update(**kwargs)
    return _conf.copy()


def load(src:int, lp:int, ch:int, rep:int):
    with file(src, lp, ch, rep) as fd:
        y = fd['recv'][...]
        x = fd['sent'][...]
        a = dict(zip(fd.attrs.keys(), fd.attrs.values())) # extract hdf attributes
    data = {'recv': y, 'sent': x, 'attr': a}

    if _conf['supdata']:
        with file(src, lp, ch, rep, supdata=True) as fd:
            nfo = fd['nfo'][...]
            data['attr']['CD'] = fd.attrs['cd']
        data.update(norm_fo=nfo)

    return data


def get(SRC, LP, CH, REP):
    ''' fetch data from remote '''
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

    for t in tqdm(targets, desc='downloading data'):
        _getfile(_datapath(*t))
        if _conf['supdata']:
            _getfile(_supdatapath(*t))


@contextlib.contextmanager
def file(src:int, lp:int, ch:int, rep:int, supdata=False):
    if supdata:
        f = _getfile(_supdatapath(src, lp, ch, rep))
    else:
        f = _getfile(_datapath(src, lp, ch, rep))
    with h5py.File(f, 'r') as fd:
        yield fd


def _validate_args(src, lp, ch, rep):
    assert src in [1, 2], f'message source index is either 1 or 2, get {src}'
    assert lp in range(-5, 4), f'launched power is from -5 to 3 (dBm), get {lp}'
    assert ch in range(1, 8), f'channel index is from 1 to 7, get {ch}'
    assert rep in [1, 2, 3], f'repeats index is from 1 to 3, get {rep}'


def _getfile(path):
    local_path = os.path.join(_conf['dump_dir'], path)
    if os.path.exists(local_path) and _conf['local']:
        f = local_path
    else:
        raw_data = dvc.api.read(path, repo=_conf['repo'], mode='rb')
        if _conf['dump']:
            _dump(raw_data, local_path)
        f = io.BytesIO(raw_data)
    return f


def _dump(data, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as fd:
        fd.write(data)


def _datapath(src, lp, ch, rep):
    _validate_args(src, lp, ch, rep)
    return 'data/1125km_src%d/%ddBm_ch%d_%d.h5' % (src, lp, ch, rep)


def _supdatapath(src, lp, ch, rep):
    _validate_args(src, lp, ch, rep)
    return 'supplementary_data/1125km_src%d/%ddBm_ch%d_%d.h5' % (src, lp, ch, rep)

