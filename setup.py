#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Installation and deployment script."""

import glob
import os
import pkg_resources
import sys

try:
  from setuptools import find_packages, setup
except ImportError:
  from distutils.core import find_packages, setup

try:
  from distutils.command.bdist_msi import bdist_msi
except ImportError:
  bdist_msi = None

try:
  from distutils.command.bdist_rpm import bdist_rpm
except ImportError:
  bdist_rpm = None

version_tuple = (sys.version_info[0], sys.version_info[1])
if version_tuple < (3, 6):
  print((
      'Unsupported Python version: {0:s}, version 3.6 or higher '
      'required.').format(sys.version))
  sys.exit(1)

# Change PYTHONPATH to include artifacts so that we can get the version.
sys.path.insert(0, '.')

import artifacts  # pylint: disable=wrong-import-position


if not bdist_msi:
  BdistMSICommand = None
else:
  class BdistMSICommand(bdist_msi):
    """Custom handler for the bdist_msi command."""

    # pylint: disable=invalid-name
    def run(self):
      """Builds an MSI."""
      # Command bdist_msi does not support the library version, neither a date
      # as a version but if we suffix it with .1 everything is fine.
      self.distribution.metadata.version += '.1'

      bdist_msi.run(self)


if not bdist_rpm:
  BdistRPMCommand = None
else:
  class BdistRPMCommand(bdist_rpm):
    """Custom handler for the bdist_rpm command."""

    # pylint: disable=invalid-name
    def _make_spec_file(self):
      """Generates the text of an RPM spec file.

      Returns:
        list[str]: lines of the RPM spec file.
      """
      # Note that bdist_rpm can be an old style class.
      if issubclass(BdistRPMCommand, object):
        spec_file = super(BdistRPMCommand, self)._make_spec_file()
      else:
        spec_file = bdist_rpm._make_spec_file(self)

      python_package = 'python3'

      description = []
      requires = ''
      summary = ''
      in_description = False

      python_spec_file = []
      for line in iter(spec_file):
        if line.startswith('Summary: '):
          summary = line[9:]

        elif line.startswith('BuildRequires: '):
          line = 'BuildRequires: {0:s}-setuptools, {0:s}-devel'.format(
              python_package)

        elif line.startswith('Requires: '):
          requires = line[10:]
          continue

        elif line.startswith('%description'):
          in_description = True

        elif line.startswith('python setup.py build'):
          if python_package == 'python3':
            line = '%py3_build'
          else:
            line = '%py2_build'

        elif line.startswith('python setup.py install'):
          if python_package == 'python3':
            line = '%py3_install'
          else:
            line = '%py2_install'

        elif line.startswith('%files'):
          lines = [
              '%files -n %{name}-data',
              '%defattr(644,root,root,755)',
              '%license LICENSE',
              '%doc ACKNOWLEDGEMENTS AUTHORS README',
              '%{_datadir}/%{name}/*',
              '',
              '%files -n {0:s}-%{{name}}'.format(python_package),
              '%defattr(644,root,root,755)',
              '%license LICENSE',
              '%doc ACKNOWLEDGEMENTS AUTHORS README']

          lines.extend([
              '%{python3_sitelib}/artifacts/*.py',
              '%{python3_sitelib}/artifacts*.egg-info/*',
              '',
              '%exclude %{_prefix}/share/doc/*',
              '%exclude %{python3_sitelib}/artifacts/__pycache__/*'])

          python_spec_file.extend(lines)
          break

        elif line.startswith('%prep'):
          in_description = False

          python_spec_file.extend([
              '%package -n %{name}-data',
              'Summary: Data files for {0:s}'.format(summary),
              '',
              '%description -n %{name}-data'])

          python_spec_file.extend(description)

          python_spec_file.append(
              '%package -n {0:s}-%{{name}}'.format(python_package))
          python_summary = 'Python 3 module of {0:s}'.format(summary)

          python_spec_file.extend([
              'Requires: artifacts-data >= %{{version}} {0:s}'.format(
                  requires),
              'Summary: {0:s}'.format(python_summary),
              '',
              '%description -n {0:s}-%{{name}}'.format(python_package)])

          python_spec_file.extend(description)

          python_spec_file.extend([
              '%package -n %{name}-tools',
              'Requires: {0:s}-artifacts >= %{{version}}'.format(
                  python_package),
              'Summary: Tools for {0:s}'.format(summary),
              '',
              '%description -n %{name}-tools'])

          python_spec_file.extend(description)

        elif in_description:
          # Ignore leading white lines in the description.
          if not description and not line:
            continue

          description.append(line)

        python_spec_file.append(line)

      python_spec_file.extend([
          '',
          '%files -n %{name}-tools',
          '%{_bindir}/*.py'])

      return python_spec_file


def parse_requirements_from_file(path):
  """Parses requirements from a requirements file.

  Args:
    path (str): path to the requirements file.

  Returns:
    list[str]: name and optional version information of the required packages.
  """
  requirements = []
  if os.path.isfile(path):
    with open(path, 'r') as file_object:
      file_contents = file_object.read()

    for requirement in pkg_resources.parse_requirements(file_contents):
      try:
        name = str(requirement.req)
      except AttributeError:
        name = str(requirement)

      if not name.startswith('pip '):
        requirements.append(name)

  return requirements


artifacts_description = (
    'ForensicArtifacts.com Artifact Repository.')

artifacts_long_description = (
    'A free, community-sourced, machine-readable knowledge base of forensic '
    'artifacts that the world can use both as an information source and within'
    ' other tools.')

setup(
    name='artifacts',
    version=artifacts.__version__,
    description=artifacts_description,
    long_description=artifacts_long_description,
    license='Apache License, Version 2.0',
    url='https://github.com/ForensicArtifacts/artifacts',
    maintainer='Forensic artifacts',
    maintainer_email='forensicartifacts@googlegroups.com',
    cmdclass={
        'bdist_msi': BdistMSICommand,
        'bdist_rpm': BdistRPMCommand},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages('.', exclude=[
        'docs', 'tests', 'tests.*', 'tools', 'utils']),
    package_dir={
        'artifacts': 'artifacts'
    },
    scripts=glob.glob(os.path.join('tools', '[a-z]*.py')),
    data_files=[
        ('share/artifacts', glob.glob(
            os.path.join('data', '*'))),
        ('share/doc/artifacts', [
            'ACKNOWLEDGEMENTS', 'AUTHORS', 'LICENSE', 'README']),
    ],
    install_requires=parse_requirements_from_file('requirements.txt'),
    tests_require=parse_requirements_from_file('test_requirements.txt'),
)
