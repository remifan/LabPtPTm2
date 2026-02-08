# LabPtPTm2

[![CC BY 4.0][cc-by-shield]][cc-by]
[![DOI](https://img.shields.io/badge/doi-10.6084/m9.figshare.14843037-blue.svg)](https://doi.org/10.6084/m9.figshare.14843037.v1)

1125km 7-channel DP-16QAM WDM transmission using quantum random bit source.
This dataset was collected in Jan 2021.

## Experimental Setup 

our experimental link
![experimental link](./assets/link.png)

setup diagram
![setup](./assets/setup.png)


## Quantum random source
the transmitted quantum random source is generated through [quantumrand](https://pypi.org/project/quantumrand/),
which wraps [ANU's QRNG restful API](https://qrng.anu.edu.au/) 


## Architecture

```mermaid
flowchart TB
    subgraph S3["AWS S3 (Remote)"]
        zarr["Zarr Store<br/>s3://optcommpubdataqrfan/labptptm2_zarr<br/>~27 GB, anonymous access"]
    end

    subgraph Cache["Local Cache Layer"]
        sc["simplecache (fsspec)<br/>on-demand download + caching"]
        clone["clone_store()<br/>full local copy"]
    end

    subgraph API["Python API (labptptm2)"]
        og["open_group()<br/>zarr.open_group wrapper<br/>consolidated metadata"]
        dl["select(SRC, LP, CH, REP)<br/>dataloader with validation"]
    end

    subgraph User["User"]
        grp["zarr.Group objects<br/>dat_grp, sup_grp"]
        data["recv[:] / sent[:]<br/>complex64 arrays"]
    end

    zarr -->|"anon=True"| sc
    zarr -->|"s3fs copy"| clone
    sc --> og
    clone --> og
    og --> dl
    dl -->|"returns"| grp
    grp -->|"lazy slicing"| data
```

## Access Data
this repo only hosts data APIs, raw data is stored in the AWS S3 remote.

### Install Data APIs
```
pip install https://github.com/remifan/labptptm2/archive/main.zip
```

### Usage
please refer to this [Instructions](examples/basics.ipynb)


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

## Acknowledgements

thanks to ANU's [QRNG web service](https://qrng.anu.edu.au/)

## See also

[LabPtPTm1](https://github.com/remifan/LabPtPTm1) - 815km DP-16QAM SSMF transmission data (Aug 2019)

## License

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

