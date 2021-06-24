# LabPtPTm2


## Setup

our experimental link
![experimental link](./assets/link.png)

setup diagram
![setup](./assets/setup.png)


## data APIs
### install
install data API through `pip`

```
pip install https://github.com/remifan/labptptm2/archive/master.zip
```

Load data. First time load might take sometime to download from remote, afterwards
it will load from local file system

```python
import labptptm2

# args 1, 0, 4, 2 means source index 1, launched power = 0 dBm, channel 4, repeats 3
data = labptptm2.load(1, 1, 4, 2)

```

### download data.
`load` calls `get` on first down loading, which simply fetches data from remote

```python
# download single data
labptptm2.get(1, 1, 4, 2) # 83 MB 

# download multiple files
labptptm2.get(1, [1, 2], [1, 4, 7], 2)

# download all datasets (24 GB)
labptptm2.get(range(1, 3), range(-5, 4), range(1, 8), range(1, 4)) 
```

### option
files are saved to `./labptptm2_data` by default, to change that

```python
labptptm2.config(dump_dir={TARGET FOLDER}) # replace {TARGET FOLDER} with your path string
```

### supplymentary data.
```python
labptptm2.config(supdata=True)

data = labptptm2.load(1, 1, 4, 2) # load data with additional supplymentary data (
                                  #   measured chromatic dispersion, frequency offset evolution)

labptptm2.load(1, 1, 3, 2) # get now downloads supplymentary data too
```

### manually load
use `file` to load file manually, for example, load small amount of data to save loading time during testing
```
with labptptm2.file(1, 1, 4, 2) as hf:
  y = fd['recv'][:num * 2]
  x = fd['sent'][:num]
  a = dict(zip(fd.attrs.keys(), fd.attrs.values())) # extract hdf attributes
# post process
# ...
```

