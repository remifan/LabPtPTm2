# LabPtPTm2

[![CC BY 4.0][cc-by-shield]][cc-by]
[![DOI](https://img.shields.io/badge/doi-10.6084/m9.figshare.14843037-blue.svg)](https://doi.org/10.6084/m9.figshare.14843037.v1)

1125km 7-channel DP-16QAM WDM transmission using quantum random bit source.
This dataset was collected in Jan 2021.

[dataloader](#data-apis) is the easiest method to access this dataset if you using Python

## Experimental Setup 

our experimental link
![experimental link](./assets/link.png)

setup diagram
![setup](./assets/setup.png)


## Quantum random source
the transmitted quantum random source is generated through [quantumrand](https://pypi.org/project/quantumrand/),
which wraps [ANU's QRNG restful API](https://qrng.anu.edu.au/) 


## Data APIs
### install
install data API through `pip`

```
pip install https://github.com/remifan/labptptm2/archive/master.zip
```

### load data
First time load might take sometime to download from remote, afterwards
it will load from local file system

```python
import labptptm2

# args 1, 0, 4, 2 means source label 1, launched power = 0 dBm, channel 4, 2nd repetition
data = labptptm2.load(1, 0, 4, 2)
```

the 4 input arguments above identify each collected sample.
- arg#1: int, random source label, which can be either 1 or 2
- arg#2: int, launched power in dBm unit, which is member of [-5, -4, -3, -2, -1, 0, 1, 2, 3]
- arg#3: int, channel index, which is member of [1, 2, 3, 4, 5, 6, 7]
- arg#4: int, index of repeated sampling under the same link configuration, can be member of [1, 2, 3]


### download data
On first downloading, `load` calls `get` which fetches data from remote

```python
# download single data (83 MB)
labptptm2.get(1, 1, 4, 2)

# `get` supports download multiple files
labptptm2.get(1, [1, 2], [1, 4, 7], 2)

# download all datasets (24 GB)
labptptm2.get(range(1, 3), range(-5, 4), range(1, 8), range(1, 4))
```

files are saved to `./labptptm2_data` by default, to change that

```python
labptptm2.config(dump_dir={TARGET FOLDER}) # replace {TARGET FOLDER} with your path string
```

to force download and overwrite the existing
```python
labptptm2.config(local=False) # load and get will always download data from remote
```

### supplymentary data
```python
labptptm2.config(supdata=True) # enable supplymentary data

data = labptptm2.load(1, 1, 4, 2) # load data with additional supplymentary data (
                                  #   measured chromatic dispersion, coarse frequency offset evolution)

labptptm2.get(1, 1, 3, 2) # get now downloads supplymentary data too
```

### load data on demand
use `file` to load a segment of data without loading the whole data from disk, for example,
one can load small amount of data to save IO overheads during testing. Such feature is realized
by [h5](https://www.h5py.org/) data format.
```python
with labptptm2.file(1, 1, 4, 2) as hf:
  y = fd['recv'][:num * 2]
  x = fd['sent'][:num]
  a = dict(zip(fd.attrs.keys(), fd.attrs.values())) # extract hdf attributes
# post processing
# ...

# open supplymentary data
with labptptm2.file(1, 1, 4, 2, supdata=True) as hf:
  nfo = fd['nfo'][...] # coarsely monitored frequency offset evolution normalized to sample period
  a['CD'] = fd.attrs['cd'] # measured chromatic dispersion
```

## About this repo
this repo does not contain the data ifself but serves as its registry, the raw data is stored in AWS S3 remote.


## Citing

```
@dataset{qrfanlabptptm2,
  author    = {Qirui Fan and Chao Lu and Alan Pak Tao Lau},
  title     = {Dataset: 1125km 7-channel DP-16QAM WDM transmission using quantum random bit source},
  year      = {2021},
  month     = "6",
  url       = "https://github.com/remifan/LabPtPTm2"
  doi       = {10.6084/m9.figshare.14843037},
  publisher = {Figshare},
}
```

## Acknowledgement

thanks to ANU's [QRNG web service](https://qrng.anu.edu.au/)


## ToDo

- add instructions for non-Python users, e.g. download data using `dvc` cli
- data APIs for Matlab (to solve: matlab's `h5read` lacks lzf filter)

## License

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

