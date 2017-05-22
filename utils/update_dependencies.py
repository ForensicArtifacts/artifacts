#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Script to update the dependencies in various configuration files."""

import os
import sys

# Change PYTHONPATH to include dependencies.
sys.path.insert(0, u'.')

import utils.dependencies  # pylint: disable=wrong-import-position


class DependencyFileWriter(object):
  """Dependency file writer."""

  def __init__(self, dependency_helper):
    """Initializes a dependency file writer.

    Args:
      dependency_helper (DependencyHelper): dependency helper.
    """
    super(DependencyFileWriter, self).__init__()
    self._dependency_helper = dependency_helper


class AppveyorYmlWriter(DependencyFileWriter):
  """Appveyor.yml file writer."""

  _PATH = os.path.join(u'appveyor.yml')

  _VERSION_PYWIN32 = u'220'
  _VERSION_WMI = u'1.4.9'

  _DOWNLOAD_PIP = (
      u'  - ps: (new-object net.webclient).DownloadFile('
      u'\'https://bootstrap.pypa.io/get-pip.py\', '
      u'\'C:\\Projects\\get-pip.py\')')

  _DOWNLOAD_PYWIN32 = (
      u'  - ps: (new-object net.webclient).DownloadFile('
      u'\'https://github.com/log2timeline/l2tbinaries/raw/master/win32/'
      u'pywin32-{0:s}.win32-py2.7.exe\', '
      u'\'C:\\Projects\\pywin32-{0:s}.win32-py2.7.exe\')').format(
          _VERSION_PYWIN32)

  _DOWNLOAD_WMI = (
      u'  - ps: (new-object net.webclient).DownloadFile('
      u'\'https://github.com/log2timeline/l2tbinaries/raw/master/win32/'
      u'WMI-{0:s}.win32.exe\', \'C:\\Projects\\WMI-{0:s}.win32.exe\')').format(
          _VERSION_WMI)

  _INSTALL_PIP = (
      u'  - cmd: "%PYTHON%\\\\python.exe C:\\\\Projects\\\\get-pip.py"')

  _INSTALL_PYWIN32 = (
      u'  - cmd: "%PYTHON%\\\\Scripts\\\\easy_install.exe '
      u'C:\\\\Projects\\\\pywin32-{0:s}.win32-py2.7.exe"').format(
          _VERSION_PYWIN32)

  _INSTALL_WMI = (
      u'  - cmd: "%PYTHON%\\\\Scripts\\\\easy_install.exe '
      u'C:\\\\Projects\\\\WMI-{0:s}.win32.exe"').format(_VERSION_WMI)

  _DOWNLOAD_L2TDEVTOOLS = (
      u'  - cmd: git clone https://github.com/log2timeline/l2tdevtools.git && '
      u'move l2tdevtools ..\\')

  _FILE_HEADER = [
      u'environment:',
      u'  matrix:',
      u'    - PYTHON: "C:\\\\Python27"',
      u'',
      u'install:',
      (u'  - cmd: \'"C:\\Program Files\\Microsoft SDKs\\Windows\\v7.1\\Bin\\'
       u'SetEnv.cmd" /x86 /release\''),
      _DOWNLOAD_PIP,
      _DOWNLOAD_PYWIN32,
      _DOWNLOAD_WMI,
      _INSTALL_PIP,
      _INSTALL_PYWIN32,
      _INSTALL_WMI,
      _DOWNLOAD_L2TDEVTOOLS]

  _L2TDEVTOOLS_UPDATE = (
      u'  - cmd: mkdir dependencies && set PYTHONPATH=..\\l2tdevtools && '
      u'"%PYTHON%\\\\python.exe" ..\\l2tdevtools\\tools\\update.py '
      u'--download-directory dependencies --machine-type x86 '
      u'--msi-targetdir "%PYTHON%" {0:s}')

  _FILE_FOOTER = [
      u'',
      u'build: off',
      u'',
      u'test_script:',
      u'  - "%PYTHON%\\\\python.exe run_tests.py"',
      u'']

  def Write(self):
    """Writes an appveyor.yml file."""
    file_content = []
    file_content.extend(self._FILE_HEADER)

    dependencies = self._dependency_helper.GetL2TBinaries()
    dependencies.extend([u'yapf'])
    dependencies = u' '.join(dependencies)

    l2tdevtools_update = self._L2TDEVTOOLS_UPDATE.format(dependencies)
    file_content.append(l2tdevtools_update)

    file_content.extend(self._FILE_FOOTER)

    file_content = u'\n'.join(file_content)
    file_content = file_content.encode(u'utf-8')

    with open(self._PATH, 'wb') as file_object:
      file_object.write(file_content)


class DPKGControlWriter(DependencyFileWriter):
  """Dpkg control file writer."""

  _PATH = os.path.join(u'config', u'dpkg', u'control')

  _PROJECT_NAME = u'artifacts'

  _MAINTAINER = u'Forensic artifacts <forensicartifacts@googlegroups.com>'

  _FILE_HEADER = [
      u'Source: {0:s}'.format(_PROJECT_NAME),
      u'Section: python',
      u'Priority: extra',
      u'Maintainer: {0:s}'.format(_MAINTAINER),
      (u'Build-Depends: debhelper (>= 7), python-all (>= 2.7~), '
       u'python-setuptools, python3-all (>= 3.4~), python3-setuptools'),
      u'Standards-Version: 3.9.5',
      u'X-Python-Version: >= 2.7',
      u'X-Python3-Version: >= 3.4',
      u'Homepage: https://github.com/ForensicArtifacts/artifacts',
      u'',
      u'Package: artifacts-data',
      u'Architecture: all',
      u'Depends: ${misc:Depends}',
      u'Description: Data files for ForensicArtifacts.com Artifact Repository',
      (u' A free, community-sourced, machine-readable knowledge base of '
       u'forensic'),
      (u' artifacts that the world can use both as an information source and '
       u'within other tools.'),
      u'']

  _PYTHON2_PACKAGE_HEADER = [
      u'Package: python-{0:s}'.format(_PROJECT_NAME),
      u'Architecture: all']

  _PYTHON3_PACKAGE_HEADER = [
      u'Package: python3-{0:s}'.format(_PROJECT_NAME),
      u'Architecture: all']

  _PYTHON_PACKAGE_DESCRIPTION = [
      (u'Description: Python bindings for ForensicArtifacts.com Artifact '
       u'Repository'),
      (u' A free, community-sourced, machine-readable knowledge base of '
       u'forensic'),
      (u' artifacts that the world can use both as an information source '
       u'and within other tools.'),
      u'']

  _PYTHON_PACKAGE_FOOTER = [
      u'Package: artifacts-tools',
      u'Architecture: all',
      (u'Depends: python-artifacts, python (>= 2.7~), ${python:Depends}, '
       u'${misc:Depends}'),
      u'Description: Tools for ForensicArtifacts.com Artifact Repository',
      (u' A free, community-sourced, machine-readable knowledge base of '
       u'forensic'),
      (u' artifacts that the world can use both as an information source and '
       u'within other tools.'),
      u'']

  def Write(self):
    """Writes a dpkg control file."""
    file_content = []
    file_content.extend(self._FILE_HEADER)
    file_content.extend(self._PYTHON2_PACKAGE_HEADER)

    dependencies = self._dependency_helper.GetDPKGDepends()
    dependencies.extend([u'${python:Depends}', u'${misc:Depends}'])
    dependencies = u', '.join(dependencies)

    file_content.append(u'Depends: artifacts-data, {0:s}'.format(dependencies))

    file_content.extend(self._PYTHON_PACKAGE_DESCRIPTION)
    file_content.extend(self._PYTHON3_PACKAGE_HEADER)

    dependencies = dependencies.replace(u'python', u'python3')

    file_content.append(u'Depends: artifacts-data, {0:s}'.format(dependencies))

    file_content.extend(self._PYTHON_PACKAGE_DESCRIPTION)
    file_content.extend(self._PYTHON_PACKAGE_FOOTER)

    file_content = u'\n'.join(file_content)
    file_content = file_content.encode(u'utf-8')

    with open(self._PATH, 'wb') as file_object:
      file_object.write(file_content)


class RequirementsWriter(DependencyFileWriter):
  """Requirements.txt file writer."""

  _PATH = u'requirements.txt'

  _FILE_HEADER = [
      u'pip >= 7.0.0',
      u'pytest',
      u'yapf']

  def Write(self):
    """Writes a requirements.txt file."""
    file_content = []
    file_content.extend(self._FILE_HEADER)

    dependencies = self._dependency_helper.GetInstallRequires()
    for dependency in dependencies:
      file_content.append(u'{0:s}'.format(dependency))

    file_content = u'\n'.join(file_content)
    file_content = file_content.encode(u'utf-8')

    with open(self._PATH, 'wb') as file_object:
      file_object.write(file_content)


class SetupCfgWriter(DependencyFileWriter):
  """Setup.cfg file writer."""

  _PATH = u'setup.cfg'

  _MAINTAINER = u'Forensic artifacts <forensicartifacts@googlegroups.com>'

  _FILE_HEADER = [
      u'[bdist_rpm]',
      u'release = 1',
      u'packager = {0:s}'.format(_MAINTAINER),
      u'doc_files = ACKNOWLEDGEMENTS',
      u'            AUTHORS',
      u'            LICENSE',
      u'            README',
      u'build_requires = python-setuptools']

  def Write(self):
    """Writes a setup.cfg file."""
    file_content = []
    file_content.extend(self._FILE_HEADER)

    dependencies = self._dependency_helper.GetRPMRequires()
    for index, dependency in enumerate(dependencies):
      if index == 0:
        file_content.append(u'requires = {0:s}'.format(dependency))
      else:
        file_content.append(u'           {0:s}'.format(dependency))

    file_content = u'\n'.join(file_content)
    file_content = file_content.encode(u'utf-8')

    with open(self._PATH, 'wb') as file_object:
      file_object.write(file_content)


class TravisBeforeInstallScriptWriter(DependencyFileWriter):
  """Travis-CI install.sh file writer."""

  _PATH = os.path.join(u'config', u'travis', u'install.sh')

  _FILE_HEADER = [
      u'#!/bin/bash',
      u'#',
      u'# Script to set up Travis-CI test VM.',
      u'',
      (u'COVERALL_DEPENDENCIES="python-coverage python-coveralls '
       u'python-docopt";'),
      u'']

  _FILE_FOOTER = [
      u'',
      u'# Exit on error.',
      u'set -e;',
      u'',
      u'if test ${TRAVIS_OS_NAME} = "osx";',
      u'then',
      u'\tgit clone https://github.com/log2timeline/l2tdevtools.git;',
      u'',
      u'\tmv l2tdevtools ../;',
      u'\tmkdir dependencies;',
      u'',
      (u'\tPYTHONPATH=../l2tdevtools ../l2tdevtools/tools/update.py '
       u'--download-directory=dependencies ${L2TBINARIES_DEPENDENCIES} '
       u'${L2TBINARIES_TEST_DEPENDENCIES};'),
      u'',
      u'elif test ${TRAVIS_OS_NAME} = "linux";',
      u'then',
      u'\tsudo add-apt-repository ppa:gift/dev -y;',
      u'\tsudo apt-get update -q;',
      u'\t# Only install the Python 2 dependencies.',
      (u'\t# Also see: https://docs.travis-ci.com/user/languages/python/'
       u'#Travis-CI-Uses-Isolated-virtualenvs'),
      (u'\tsudo apt-get install -y ${COVERALL_DEPENDENCIES} '
       u'${PYTHON2_DEPENDENCIES} ${PYTHON2_TEST_DEPENDENCIES};'),
      u'fi',
      u'']

  def Write(self):
    """Writes an install.sh file."""
    file_content = []
    file_content.extend(self._FILE_HEADER)

    dependencies = self._dependency_helper.GetL2TBinaries()
    dependencies = u' '.join(dependencies)
    file_content.append(u'L2TBINARIES_DEPENDENCIES="{0:s}";'.format(
        dependencies))

    file_content.append(u'')
    file_content.append(u'L2TBINARIES_TEST_DEPENDENCIES="yapf";')

    file_content.append(u'')

    dependencies = self._dependency_helper.GetDPKGDepends(exclude_version=True)
    dependencies = u' '.join(dependencies)
    file_content.append(u'PYTHON2_DEPENDENCIES="{0:s}";'.format(dependencies))

    file_content.append(u'')
    file_content.append(u'PYTHON2_TEST_DEPENDENCIES="python-yapf";')

    file_content.extend(self._FILE_FOOTER)

    file_content = u'\n'.join(file_content)
    file_content = file_content.encode(u'utf-8')

    with open(self._PATH, 'wb') as file_object:
      file_object.write(file_content)


if __name__ == u'__main__':
  helper = utils.dependencies.DependencyHelper()

  for writer_class in (
      AppveyorYmlWriter, DPKGControlWriter, RequirementsWriter, SetupCfgWriter,
      TravisBeforeInstallScriptWriter):
    writer = writer_class(helper)
    writer.Write()
