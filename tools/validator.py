#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tool to validate artifact definitions."""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import os
import sys

from artifacts import definitions
from artifacts import errors
from artifacts import reader
from artifacts import registry


class ArtifactDefinitionsValidator(object):
  """Artifact definitions validator."""

  LEGACY_PATH = os.path.join('data', 'legacy.yaml')

  _MACOS_PRIVATE_SUB_PATHS = ('etc', 'tftpboot', 'tmp', 'var')

  def __init__(self):
    """Initializes an artifact definitions validator."""
    super(ArtifactDefinitionsValidator, self).__init__()
    self._artifact_registry = registry.ArtifactDefinitionsRegistry()
    self._artifact_registry_key_paths = set()

  def _CheckRegistryKeyPath(self, filename, artifact_definition, key_path):
    """Checks a Windows Registry key path.

    Args:
      filename (str): name of the artifacts definition file.
      artifact_definition (ArtifactDefinition): artifact definition.
      key_path (str): key path.

    Returns:
      bool: True if the Registry key path is valid.
    """
    result = True
    key_path = key_path.upper()

    if key_path.startswith('%%CURRENT_CONTROL_SET%%'):
      result = False
      logging.warning((
          'Artifact definition: {0:s} in file: {1:s} contains Windows '
          'Registry key path that starts with '
          '%%CURRENT_CONTROL_SET%%. Replace %%CURRENT_CONTROL_SET%% with '
          'HKEY_LOCAL_MACHINE\\System\\CurrentControlSet').format(
              artifact_definition.name, filename))

    return result

  def _CheckMacOSPaths(self, filename, artifact_definition, source, paths):
    """Checks if the paths are valid MacOS paths.

    Args:
      filename (str): name of the artifacts definition file.
      artifact_definition (ArtifactDefinition): artifact definition.
      source (SourceType): source definition.
      paths (list[str]): paths to validate.

    Returns:
      bool: True if the MacOS paths is valid.
    """
    result = True

    paths_with_private = []
    paths_with_symbolic_link_to_private = []

    for path in paths:
      path_lower = path.lower()
      path_segments = path_lower.split(source.separator)
      if not path_segments:
        logging.warning((
            'Empty path defined by artifact definition: {0:s} in file: '
            '{1:s}').format(artifact_definition.name, filename))
        result = False

      elif len(path_segments) == 1:
        continue

      elif path_segments[1] in self._MACOS_PRIVATE_SUB_PATHS:
        paths_with_symbolic_link_to_private.append(path)

      elif path_segments[1] == 'private' and len(path_segments) >= 2:
        if path_segments[2] in self._MACOS_PRIVATE_SUB_PATHS:
          paths_with_private.append(path)

        else:
          logging.warning((
              'Unsupported private path: {0:s} defined by artifact definition: '
              '{1:s} in file: {2:s}').format(
                  path, artifact_definition.name, filename))
          result = False

    for private_path in paths_with_private:
      if private_path[8:] not in paths_with_symbolic_link_to_private:
        logging.warning((
            'Missing symbolic link: {0:s} for path: {1:s} defined by artifact '
            'definition: {2:s} in file: {3:s}').format(
                private_path[8:], private_path, artifact_definition.name,
                filename))
        result = False

    for path in paths_with_symbolic_link_to_private:
      private_path = '/private{0:s}'.format(path)
      if private_path not in paths_with_private:
        logging.warning((
            'Missing path: {0:s} for symbolic link: {1:s} defined by artifact '
            'definition: {2:s} in file: {3:s}').format(
                private_path, path, artifact_definition.name, filename))
        result = False

    return result

  def _CheckWindowsPath(self, filename, artifact_definition, source, path):
    """Checks if a path is a valid Windows path.

    Args:
      filename (str): name of the artifacts definition file.
      artifact_definition (ArtifactDefinition): artifact definition.
      source (SourceType): source definition.
      path (str): path to validate.

    Returns:
      bool: True if the Windows path is valid.
    """
    result = True

    number_of_forward_slashes = path.count('/')
    number_of_backslashes = path.count('\\')
    if (number_of_forward_slashes < number_of_backslashes and
        source.separator != '\\'):
      logging.warning((
          'Incorrect path separator: {0:s} in path: {1:s} defined '
          'by artifact definition: {2:s} in file: {3:s}').format(
              source.separator, path, artifact_definition.name,
              filename))
      result = False

    if source.separator != '\\':
      return result

    path_lower = path.lower()
    path_segments = path_lower.split(source.separator)
    if not path_segments:
      logging.warning((
          'Empty path defined by artifact definition: {0:s} in file: '
          '{1:s}').format(artifact_definition.name, filename))
      result = False

    elif path_segments[0].startswith('%%users.') and path_segments[0] not in (
        '%%users.appdata%%', '%%users.homedir%%', '%%users.localappdata%%',
        '%%users.temp%%', '%%users.username%%', '%%users.userprofile%%'):
      logging.warning((
          'Unsupported "{0:s}" in path: {1:s} defined by artifact '
          'definition: {2:s} in file: {3:s}').format(
              path_segments[0], path, artifact_definition.name, filename))
      result = False

    elif path_segments[0] == '%%users.homedir%%':
      logging.warning((
          'Replace "%%users.homedir%%" by "%%users.userprofile%%" in path: '
          '{0:s} defined by artifact definition: {1:s} in file: '
          '{2:s}').format(path, artifact_definition.name, filename))
      result = False

    elif path_lower.startswith('%%users.userprofile%%\\appdata\\local\\'):
      logging.warning((
          'Replace "%%users.userprofile%%\\AppData\\Local" by '
          '"%%users.localappdata%%" in path: {0:s} defined by artifact '
          'definition: {1:s} in file: {2:s}').format(
              path, artifact_definition.name, filename))
      result = False

    elif path_lower.startswith('%%users.userprofile%%\\appdata\\roaming\\'):
      logging.warning((
          'Replace "%%users.userprofile%%\\AppData\\Roaming" by '
          '"%%users.appdata%%" in path: {0:s} defined by artifact '
          'definition: {1:s} in file: {2:s}').format(
              path, artifact_definition.name, filename))
      result = False

    elif path_lower.startswith('%%users.userprofile%%\\application data\\'):
      logging.warning((
          'Replace "%%users.userprofile%%\\Application Data" by '
          '"%%users.appdata%%" in path: {0:s} defined by artifact '
          'definition: {1:s} in file: {2:s}').format(
              path, artifact_definition.name, filename))
      result = False

    elif path_lower.startswith(
        '%%users.userprofile%%\\local settings\\application data\\'):
      logging.warning((
          'Replace "%%users.userprofile%%\\Local Settings\\Application Data" '
          'by "%%users.localappdata%%" in path: {0:s} defined by artifact '
          'definition: {1:s} in file: {2:s}').format(
              path, artifact_definition.name, filename))
      result = False

    return result

  def _HasDuplicateRegistryKeyPaths(
      self, filename, artifact_definition, source):
    """Checks if Registry key paths are not already defined by other artifacts.

    Note that at the moment this function will only find exact duplicate
    Registry key paths.

    Args:
      filename (str): name of the artifacts definition file.
      artifact_definition (ArtifactDefinition): artifact definition.
      source (SourceType): source definition.

    Returns:
      bool: True if the Registry key paths defined by the source type
          are used in other artifacts.
    """
    result = False
    intersection = self._artifact_registry_key_paths.intersection(
        set(source.keys))
    if intersection:
      duplicate_key_paths = '\n'.join(intersection)
      logging.warning((
          'Artifact definition: {0:s} in file: {1:s} has duplicate '
          'Registry key paths:\n{2:s}').format(
              artifact_definition.name, filename, duplicate_key_paths))
      result = True

    self._artifact_registry_key_paths.update(source.keys)
    return result

  def CheckFile(self, filename):
    """Validates the artifacts definition in a specific file.

    Args:
      filename (str): name of the artifacts definition file.

    Returns:
      bool: True if the file contains valid artifacts definitions.
    """
    result = True
    artifact_reader = reader.YamlArtifactsReader()

    try:
      for artifact_definition in artifact_reader.ReadFile(filename):
        try:
          self._artifact_registry.RegisterDefinition(artifact_definition)
        except KeyError:
          logging.warning(
              'Duplicate artifact definition: {0:s} in file: {1:s}'.format(
                  artifact_definition.name, filename))
          result = False

        artifact_definition_supports_macos = (
            definitions.SUPPORTED_OS_DARWIN in (
                artifact_definition.supported_os))
        artifact_definition_supports_windows = (
            definitions.SUPPORTED_OS_WINDOWS in (
                artifact_definition.supported_os))

        for source in artifact_definition.sources:
          if source.type_indicator in (
              definitions.TYPE_INDICATOR_FILE, definitions.TYPE_INDICATOR_PATH):

            if (definitions.SUPPORTED_OS_DARWIN in source.supported_os or (
                artifact_definition_supports_macos and
                not source.supported_os)):
              if not self._CheckMacOSPaths(
                  filename, artifact_definition, source, source.paths):
                result = False

            elif (artifact_definition_supports_windows or
                  definitions.SUPPORTED_OS_WINDOWS in source.supported_os):
              for path in source.paths:
                if not self._CheckWindowsPath(
                    filename, artifact_definition, source, path):
                  result = False

          elif source.type_indicator == (
              definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY):

            # Exempt the legacy file from duplicate checking because it has
            # duplicates intentionally.
            if (filename != self.LEGACY_PATH and
                self._HasDuplicateRegistryKeyPaths(
                    filename, artifact_definition, source)):
              result = False

            for key_path in source.keys:
              if not self._CheckRegistryKeyPath(
                  filename, artifact_definition, key_path):
                result = False

          elif source.type_indicator == (
              definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE):

            for key_value_pair in source.key_value_pairs:
              if not self._CheckRegistryKeyPath(
                  filename, artifact_definition, key_value_pair['key']):
                result = False

    except errors.FormatError as exception:
      logging.warning(
          'Unable to validate file: {0:s} with error: {1!s}'.format(
              filename, exception))
      result = False

    return result

  def GetUndefinedArtifacts(self):
    """Retrieves the names of undefined artifacts used by artifact groups.

    Returns:
      set[str]: undefined artifacts names.
    """
    return self._artifact_registry.GetUndefinedArtifacts()


def Main():
  """The main program function.

  Returns:
    bool: True if successful or False if not.
  """
  args_parser = argparse.ArgumentParser(
      description='Validates an artifact definitions file.')

  args_parser.add_argument(
      'filename',
      nargs='?',
      action='store',
      metavar='artifacts.yaml',
      default=None,
      help=('path of the file that contains the artifact '
            'definitions.'))

  options = args_parser.parse_args()

  if not options.filename:
    print('Source value is missing.')
    print('')
    args_parser.print_help()
    print('')
    return False

  if not os.path.isfile(options.filename):
    print('No such file: {0:s}'.format(options.filename))
    print('')
    return False

  print('Validating: {0:s}'.format(options.filename))
  validator = ArtifactDefinitionsValidator()
  if not validator.CheckFile(options.filename):
    print('FAILURE')
    return False

  print('SUCCESS')
  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
