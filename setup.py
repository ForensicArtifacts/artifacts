#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 The ForensicArtifacts.com Artifact Repository project.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Installation and deployment script."""

import glob
import os
import sys

import run_tests

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
  artifacts_version += '.1'

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
    cmdclass={'test': TestCommand},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    package_dir={'artifacts': 'artifacts'},
    packages=find_packages('.'),
)
