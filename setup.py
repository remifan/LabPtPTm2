# coding=utf-8
"""Install LabPtPtm2."""

from setuptools import setup, find_packages

setup(name='labptptm2',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'h5py',
        'dvc'
    ]
)
