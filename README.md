# LabPtPTm2

[![CC BY 4.0][cc-by-shield]][cc-by]

LabPtPTm2(Lab dataset series - point to point 1125km-SSMF 7-channel WDM transmission data)

this dataset is collected in Jan 2021.


## Setup

our experimental link
![experimental link](./assets/link.png)

setup diagram
![setup](./assets/setup.png)


## Quantum random source
the transmitted quantum random source is generated through [quantumrand](https://pypi.org/project/quantumrand/),
which wraps [ANU's QRNG API](https://qrng.anu.edu.au/) 


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

# args 1, 0, 4, 2 means source index 1, launched power = 0 dBm, channel 4, repeats 3
data = labptptm2.load(1, 1, 4, 2)

```

### download data.
`load` calls `get` on first down loading, which simply fetches data from remote

```python
# download single data (83 MB)
labptptm2.get(1, 1, 4, 2)

# download multiple files
labptptm2.get(1, [1, 2], [1, 4, 7], 2)

# download all datasets (24 GB)
labptptm2.get(range(1, 3), range(-5, 4), range(1, 8), range(1, 4)) 
```

files are saved to `./labptptm2_data` by default, to change that

```python
labptptm2.config(dump_dir={TARGET FOLDER}) # replace {TARGET FOLDER} with your path string
```

### supplymentary data
```python
labptptm2.config(supdata=True) # enable supplymentary data

data = labptptm2.load(1, 1, 4, 2) # load data with additional supplymentary data (
                                  #   measured chromatic dispersion, frequency offset evolution)

labptptm2.load(1, 1, 3, 2) # get now downloads supplymentary data too
```

### manually open data file
use `file` to load file manually, for example, load small amount of data to save loading time during testing
```python
with labptptm2.file(1, 1, 4, 2) as hf:
  y = fd['recv'][:num * 2]
  x = fd['sent'][:num]
  a = dict(zip(fd.attrs.keys(), fd.attrs.values())) # extract hdf attributes
# post process
# ...

# open supplymentary data
with labptptm2.file(1, 1, 4, 2, supdata=True) as hf:
  nfo = fd['nfo'][...] # coarsely monitored frequency offset evolution normalized to sample period
  a['CD'] = fd.attrs['cd'] # measured chromatic dispersion
```

## License

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

