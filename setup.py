#!/usr/bin/env python
from codecs import open
from os import path
from setuptools import setup, find_packages

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='searchsplunk',
    version='0.3.1',
    description='Splunk search client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ryan Currah',
    author_email='ryan@currah.ca',
    url='https://github.com/ryancurrah/searchsplunk',
    license='GPLv2',
    keywords=['splunk', 'search'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    packages=find_packages(),
    install_requires=[
        'requests>=2.7.0'
    ]
)
