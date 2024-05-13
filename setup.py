## setup.py
from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup

setup(
    name='OneLoader',
    version='0.1',
    packages=find_packages(include=['one_api', 'one_api.*', 'oneloader_runner', 'oneloader_runner.*'])
)