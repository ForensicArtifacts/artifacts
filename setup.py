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

try:
  from setuptools.commands.bdist_rpm import bdist_rpm
except ImportError:
  from distutils.command.bdist_rpm import bdist_rpm

# Change PYTHONPATH to include artifacts so that we can get the version.
sys.path.insert(0, '.')

import artifacts


class BdistRPMCommand(bdist_rpm):
  """Custom handler for the bdist_rpm command."""

  def _make_spec_file(self):
    """Generates the text of an RPM spec file.

    Returns:
      A list of strings containing the lines of text.
    """
    # Note that bdist_rpm can be an old style class.
    if issubclass(BdistRPMCommand, object):
      spec_file = super(BdistRPMCommand, self)._make_spec_file()
    else:
      spec_file = bdist_rpm._make_spec_file(self)

    if sys.version_info[0] < 3:
      python_package = 'python'
    else:
      python_package = 'python3'

    description = []
    summary = ''
    in_description = False

    python_spec_file = []
    for index, line in enumerate(spec_file):
      if line.startswith('Summary: '):
        summary = line

      elif line.startswith('BuildRequires: '):
        line = 'BuildRequires: {0:s}-setuptools'.format(python_package)

      elif line.startswith('Requires: '):
        if python_package == 'python3':
          line = line.replace('python', 'python3')

      elif line.startswith('%description'):
        in_description = True

      elif line.startswith('%files'):
        line = '%files -f INSTALLED_FILES -n {0:s}-%{{name}}'.format(
           python_package)

      elif line.startswith('%prep'):
        in_description = False

        python_spec_file.append(
            '%package -n {0:s}-%{{name}}'.format(python_package))
        python_spec_file.append('{0:s}'.format(summary))
        python_spec_file.append('')
        python_spec_file.append(
            '%description -n {0:s}-%{{name}}'.format(python_package))
        python_spec_file.extend(description)

      elif in_description:
        # Ignore leading white lines in the description.
        if not description and not line:
          continue

        description.append(line)

      python_spec_file.append(line)

    return python_spec_file


artifacts_version = artifacts.__version__

# Command bdist_msi does not support the library version, neither a date
# as a version but if we suffix it with .1 everything is fine.
if 'bdist_msi' in sys.argv:
  artifacts_version = '{0}.1'.format(artifacts_version)

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
        os.path.join('tools', 'stats.py'),
        os.path.join('tools', 'validator.py'),
    ],
    cmdclass={'bdist_rpm': BdistRPMCommand},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages('.', exclude=[
        'tests', 'tests.*', 'tools', 'utils']),
    package_dir={'artifacts': 'artifacts'},
    data_files=[
        ('share/artifacts', glob.glob(os.path.join('data', '*'))),
    ],
    install_requires=[
        'PyYAML >= 3.11',
    ],
)
