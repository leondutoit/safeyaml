#!/usr/bin/env python
# Ref: https://docs.python.org/2/distutils/setupscript.html

from setuptools import setup

setup(
    name='safeyaml',
    version='0.1.0',
    description='Load YAML config safely',
    author='Leon du Toit',
    author_email='dutoit.leon@gmail.com',
    url='https://github.com/leondutoit/safeyaml',
    packages=['safeyaml'],
    package_data={
        'safeyaml': [
            'tests/*.py'
        ]
    },
)
