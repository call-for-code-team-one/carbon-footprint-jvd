"""
Carbon Footprint Calculator app for running Python apps on Bluemix
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, '../README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='carbon_footprint_app-jvd',
    version='1.0.0',
    description='Carbon Footprint Calculator app for running Python apps on Bluemix',
    long_description=long_description,
    url='https://github.com/call-for-code-team-one/carbon-footprint-jvd.git'
)