#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='searchsplunk',
    version='0.1.0',
    description='Splunk search client',
    author='Ryan Currah',
    author_email='ryan@currah.ca',
    url='https://github.com/ryancurrah/searchsplunk',
    keywords=['splunk', 'search'],
    classifiers=['License :: OSI Approved :: GNU General Public License version 2'],
    packages=find_packages(),
    install_requires=[
        'requests>=2.7.0'
    ]
)
