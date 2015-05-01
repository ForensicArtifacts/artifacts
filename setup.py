#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Installation and deployment script."""

import glob
import os
import sys

try:
  from setuptools import find_packages, setup, Command
except ImportError:
  from distutils.core import find_packages, setup, Command

# Change PYTHONPATH to include artifacts so that we can get the version.
sys.path.insert(0, '.')

import artifacts


artifacts_version = artifacts.__version__

# Command bdist_msi does not support the library version, neither a date
# as a version but if we suffix it with .1 everything is fine.
if 'bdist_msi' in sys.argv:
  artifacts_version = '{0:s}.1'.format(artifacts_version)

artifacts_description = (
    'ForensicArtifacts.com Artifact Repository.')

artifacts_long_description = (
    'A free, community-sourced, machine-readable knowledge base of forensic '
    'artifacts that the world can use both as an information source and '
    'within other tools.')

setup(
    name='artifacts',
    version=artifacts_version,
    description=artifacts_description,
    long_description=artifacts_long_description,
    license='Apache License, Version 2.0',
    url='https://github.com/ForensicArtifacts/artifacts',
    maintainer='The ForensicArtifacts.com Artifact Repository project',
    maintainer_email='forensicartifacts@googlegroups.com',
    scripts=[
        os.path.join('tools', 'validator.py'),
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages('.', exclude=[u'tools']),
    package_dir={'artifacts': 'artifacts'},
    data_files=[
        ('share/artifacts', glob.glob(os.path.join('definitions', '*'))),
    ],
    install_requires=[
        'PyYAML >= 3.11',
    ],
)
