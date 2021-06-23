import os
import io
import h5py
import dvc.api
import contextlib
from pathlib import Path


repo = 'https://github.com/remifan/LabPtPTm2'
dump_dir = os.path.join(os.getcwd(), 'labptptm2_data')


def load(src,
         lp,
         ch,
         rep,
         supdata=False,
         local=True,
         dump=False):

    with _read(_datapath(src, lp, ch, rep),
               local,
               dump) as fd:
        y = fd['recv'][...]
        x = fd['sent'][...]
        a = dict(zip(fd.attrs.keys(), fd.attrs.values())) # extract hdf attributes

    data = {'recv': y, 'sent': x, 'attr': a}

    if supdata:
        with _read(_supdatapath(src, lp, ch, rep),
                   local,
                   dump) as fd:
            nfo = fd['nfo'][...]
            data['attr']['CD'] = fd.attrs['cd']

        data.update(norm_fo=nfo)

    return data


@contextlib.contextmanager
def _read(path, local=True, dump=False):
    local_path = os.path.join(dump_dir, path)
    if os.path.exists(local_path) and local:
        file = local_path
    else:
        raw_data = dvc.api.read(path, repo=repo, mode='rb')
        if dump:
            _dump(raw_data, local_path)
        file = io.BytesIO(raw_data)

    with h5py.File(file, 'r') as fd:
        yield fd


def _dump(data, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as fd:
        fd.write(data)


def _datapath(src, lp, ch, rep):
    return 'data/1125km_src%d/%ddBm_ch%d_%d.h5' % (src, lp, ch, rep)


def _supdatapath(src, lp, ch, rep):
    return 'supplementary_data/1125km_src%d/%ddBm_ch%d_%d.h5' % (src, lp, ch, rep)

