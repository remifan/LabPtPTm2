# coding=utf-8
"""Install LabPtPtm2."""

from setuptools import setup, find_packages

setup(name='labptptm2',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'zarr[jupyter]==2.9.5',
        'fsspec',
        's3fs',
        'pyyaml'
    ]
)
