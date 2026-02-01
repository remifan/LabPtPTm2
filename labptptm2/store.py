import os
import io
import yaml
import logging
import tempfile
import warnings
import zarr
import s3fs
import fsspec


tempdir = os.path.join(tempfile.gettempdir(),'labptptm2')


class Config:
    __slots__ = ['store', 'remote', 'cache_storage']
    
    def __init__(self):
        self.store = None 
        self.remote = "s3://optcommpubdataqrfan/labptptm2_zarr" 
        self.cache_storage = tempdir
        self.load()
        if self.store is None or os.path.normpath(self.store) == os.path.normpath(tempdir):
            logging.warning((f'Data would be auto-cached in default temporary location: {self.cache_storage}, '
                             f'set labptptm2.config.cache_storage to other locations to suppress this warning'))

    def _update(self, d):
        for k in self.__slots__:
            if k in d:
                setattr(self, k, d[k])

    def load(self):
        for f in self.config_file_search_paths():
            # Read YAML file
            filename = os.path.join(f, "labptptm2.yaml")
            if os.path.exists(filename):
                with open(filename, 'r') as stream:
                    conf = yaml.safe_load(stream)
                    self._update(conf)
                break

    def dump(self, tardir=os.getcwd()):
        dump_path = os.path.join(tardir, 'labptptm2.yaml')
        d = {}
        for k in self.__slots__:
            d[k] = getattr(self, k)
        with io.open(dump_path, 'w', encoding='utf8') as outfile:
            yaml.dump(d, outfile, default_flow_style=False, allow_unicode=True)
        logging.info(f'dump config to {dump_path}')

    def config_file_search_paths(self):
        paths = []
        cwd = os.getcwd()
        paths.append(cwd)
        return paths

    def __repr__(self):
        return f"store: {self.store}\nremote: {self.remote}\ncache_storage: {self.cache_storage}"


config = Config()


def open_group(store=None, **kwargs):
    ''' the read-only version of zarr.open_group

    The dataset should have been consolidated which enables fastest metadata
    navigation without traversing the actual data.

    References:
      https://zarr.readthedocs.io/en/stable/tutorial.html#consolidating-metadata
    '''

    if store is None:
        store = config.store

    if store is None:
        # open remote store with local cache layer;
        # reference:
        #   https://zarr.readthedocs.io/en/stable/tutorial.html#io-with-fsspec
        #   https://filesystem-spec.readthedocs.io/en/latest/features.html#caching-files-locally
        # Note: suppress the async warning from zarr since simplecache doesn't support async mode
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', message='.*asynchronous.*', category=UserWarning)
            root = zarr.open_group("simplecache::" + config.remote,
                                   mode='r',
                                   storage_options={"s3": {'anon': True},
                                                    "simplecache": {'cache_storage': config.cache_storage}},
                                   use_consolidated=True,
                                   zarr_format=2,
                                   **kwargs)
    else:
        # open local store
        root = zarr.open_group(store, mode='r', use_consolidated=True, zarr_format=2, **kwargs)

    return root


def clone_store(dest, log=None, **kwargs):
    '''Clone the entire remote store to a local directory.

    Uses fsspec to copy files from S3 to local storage.

    Parameters
    ----------
    dest : str
        Destination directory path
    log : file-like, optional
        File object to write progress logs (e.g., sys.stdout)
    '''
    os.makedirs(dest, exist_ok=True)
    s3 = s3fs.S3FileSystem(anon=True)
    remote_path = config.remote.replace('s3://', '')

    # Get list of all files in the remote store
    all_files = s3.find(remote_path)

    for i, remote_file in enumerate(all_files):
        # Compute relative path and local destination
        rel_path = remote_file[len(remote_path):].lstrip('/')
        local_path = os.path.join(dest, rel_path)

        # Create parent directories if needed
        local_dir = os.path.dirname(local_path)
        if local_dir:
            os.makedirs(local_dir, exist_ok=True)

        # Copy file
        s3.get(remote_file, local_path)

        if log is not None:
            log.write(f"\r[{i+1}/{len(all_files)}] Copying: {rel_path}")
            log.flush()

    if log is not None:
        log.write("\nDone.\n")
        log.flush()


