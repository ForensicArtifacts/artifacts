#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tool to validate artifact definitions."""

import argparse
import glob
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

  _SUPPORTED_POSIX_USERS_VARIABLES = [
      '%%users.homedir%%']

  _SUPPORTED_WINDOWS_ENVIRONMENT_VARIABLES = [
      '%%environ_allusersappdata%%',
      '%%environ_allusersprofile%%',
      '%%environ_programfiles%%',
      '%%environ_programfilesx86%%',
      '%%environ_systemdrive%%',
      '%%environ_systemroot%%',
      '%%environ_windir%%']

  _SUPPORTED_WINDOWS_USERS_VARIABLES = [
      '%%users.appdata%%',
      '%%users.localappdata%%',
      '%%users.sid%%',
      '%%users.temp%%',
      '%%users.username%%',
      '%%users.userprofile%%']

  def __init__(self):
    """Initializes an artifact definitions validator."""
    super(ArtifactDefinitionsValidator, self).__init__()
    self._artifact_registry = registry.ArtifactDefinitionsRegistry()
    self._artifact_registry_key_paths = set()

  def _CheckGlobstarInPathSegment(
      self, filename, artifact_definition, path, path_segment):
    """Checks if a globstar in a path segment is valid.

    Args:
      filename (str): name of the artifacts definition file.
      artifact_definition (ArtifactDefinition): artifact definition.
      path (str): path of which the path segment originated.
      path_segment (str): path segment to validate.

    Returns:
      bool: True if the globstar is valid.
    """
    if not path_segment.startswith('**'):
      logging.warning((
          'Unuspported globstar with prefix: {0:s} for path: {1:s} defined by '
          'artifact definition: {2:s} in file: {3:s}').format(
              path_segment, path, artifact_definition.name, filename))
      return False

    if len(path_segment) > 2:
      try:
        recursion_depth = int(path_segment[2:], 10)
      except (TypeError, ValueError):
        logging.warning((
            'Unuspported globstar with suffix: {0:s} for path: {1:s} defined '
            'by artifact definition: {2:s} in file: {3:s}').format(
                path_segment, path, artifact_definition.name, filename))
        return False

      if recursion_depth <= 0 or recursion_depth > 10:
        logging.warning((
            'Globstar with unsupported recursion depth: {0:s} for path: {1:s} '
            'defined by artifact definition: {2:s} in file: {3:s}').format(
                path_segment, path, artifact_definition.name, filename))
        return False

    return True

  def _CheckMacOSPaths(self, filename, artifact_definition, paths):
    """Checks if the paths are valid MacOS paths.

    Args:
      filename (str): name of the artifacts definition file.
      artifact_definition (ArtifactDefinition): artifact definition.
      paths (list[str]): paths to validate.

    Returns:
      bool: True if the MacOS paths is valid.
    """
    result = True

    paths_with_private = []
    paths_with_symbolic_link_to_private = []

    for path in paths:
      path_lower = path.lower()
      path_segments = path_lower.split('/')
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

      has_globstar = False
      for path_segment in path_segments:
        if '**' in path_segment:
          if has_globstar:
            logging.warning((
                'Unsupported path: {0:s} with multiple globstars defined by '
                'artifact definition: {1:s} in file: {2:s}').format(
                    path, artifact_definition.name, filename))
            result = False
            break

          has_globstar = True
          if not self._CheckGlobstarInPathSegment(
              filename, artifact_definition, path, path_segment):
            result = False

      if has_globstar and path.endswith('/'):
        logging.warning((
            'Unsupported path: {0:s} with globstar and trailing path '
            'separator defined by artifact definition: {1:s} in file: '
            '{2:s}').format(path, artifact_definition.name, filename))
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

  def _CheckPath(self, filename, artifact_definition, source, path):
    """Checks if a path is valid.

    Args:
      filename (str): name of the artifacts definition file.
      artifact_definition (ArtifactDefinition): artifact definition.
      source (SourceType): source definition.
      path (str): path to validate.

    Returns:
      bool: True if the path is valid.
    """
    result = True

    path_segments = path.split(source.separator)

    has_globstar = False
    for path_segment in path_segments:
      if '**' in path_segment:
        if has_globstar:
          logging.warning((
              'Unsupported path: {0:s} with multiple globstars defined by '
              'artifact definition: {1:s} in file: {2:s}').format(
                  path, artifact_definition.name, filename))
          result = False
          break

        has_globstar = True
        if not self._CheckGlobstarInPathSegment(
            filename, artifact_definition, path, path_segment):
          result = False

    if has_globstar and path.endswith(source.separator):
      logging.warning((
          'Unsupported path: {0:s} with globstar and trailing path '
          'separator defined by artifact definition: {1:s} in file: '
          '{2:s}').format(path, artifact_definition.name, filename))
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

    has_globstar = False
    for path_segment in path_segments:
      if path_segment.startswith('%%') and path_segment.endswith('%%'):
        if (path_segment.startswith('%%environ_') and
            path_segment not in self._SUPPORTED_WINDOWS_ENVIRONMENT_VARIABLES):
          result = False
          logging.warning((
              'Artifact definition: {0:s} in file: {1:s} contains Windows '
              'path that contains an unuspported environment variable: '
              '"{2:s}".').format(
                  artifact_definition.name, filename, path_segment))

        elif (path_segment.startswith('%%users.') and
              path_segment not in self._SUPPORTED_WINDOWS_USERS_VARIABLES):
          result = False
          logging.warning((
              'Artifact definition: {0:s} in file: {1:s} contains Windows '
              'path that contains an unsupported users variable: '
              '"{2:s}". ').format(
                  artifact_definition.name, filename, path_segment))

      elif '**' in path_segment:
        if has_globstar:
          logging.warning((
              'Unsupported path: {0:s} with multiple globstars defined by '
              'artifact definition: {1:s} in file: {2:s}').format(
                  path, artifact_definition.name, filename))
          result = False
          break

        has_globstar = True
        if not self._CheckGlobstarInPathSegment(
            filename, artifact_definition, path, path_segment):
          result = False

    if has_globstar and path.endswith(source.separator):
      logging.warning((
          'Unsupported path: {0:s} with globstar and trailing path '
          'separator defined by artifact definition: {1:s} in file: '
          '{2:s}').format(path, artifact_definition.name, filename))
      result = False

    return result

  def _CheckWindowsRegistryKeyPath(
      self, filename, artifact_definition, key_path):
    """Checks if a path is a valid Windows Registry key path.

    Args:
      filename (str): name of the artifacts definition file.
      artifact_definition (ArtifactDefinition): artifact definition.
      key_path (str): Windows Registry key path to validate.

    Returns:
      bool: True if the Windows Registry key path is valid.
    """
    result = True
    key_path_segments = key_path.lower().split('\\')

    if key_path_segments[0] == '%%current_control_set%%':
      result = False
      logging.warning((
          'Artifact definition: {0:s} in file: {1:s} contains Windows '
          'Registry key path that starts with '
          '%%CURRENT_CONTROL_SET%%. Replace %%CURRENT_CONTROL_SET%% with '
          'HKEY_LOCAL_MACHINE\\System\\CurrentControlSet').format(
              artifact_definition.name, filename))

    for segment_index, key_path_segment in enumerate(key_path_segments):
      if key_path_segment.startswith('%%') and key_path_segment.endswith('%%'):
        if (segment_index == 1 and key_path_segment == '%%users.sid%%' and
            key_path_segments[0] == 'hkey_users'):
          continue

        if key_path_segment.startswith('%%environ_'):
          result = False
          logging.warning((
              'Artifact definition: {0:s} in file: {1:s} contains Windows '
              'Registry key path that contains an environment variable: '
              '"{2:s}". Usage of environment variables in key paths is not '
              'encouraged at this time.').format(
                  artifact_definition.name, filename, key_path_segment))

        elif key_path_segment.startswith('%%users.'):
          result = False
          logging.warning((
              'Artifact definition: {0:s} in file: {1:s} contains Windows '
              'Registry key path that contains a users variable: "{2:s}". '
              'Usage of users variables in key paths, except for '
              '"HKEY_USERS\\%%users.sid%%", is not encouraged at this '
              'time.').format(
                  artifact_definition.name, filename, key_path_segment))

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

  def CheckDirectory(self, path):
    """Validates the artifacts definition in a specific directory.

    Args:
      path (str): path of the directory containing the artifacts definition
          files.

    Returns:
      bool: True if the file contains valid artifacts definitions.
    """
    for filename in glob.glob(os.path.join(path, '*.yaml')):
      result = self.CheckFile(filename)
      if not result:
        break

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

        macos_paths = []

        for source in artifact_definition.sources:
          if source.type_indicator == definitions.TYPE_INDICATOR_DIRECTORY:
            logging.warning((
                'Use of deprecated source type: DIRECTORY in artifact '
                'definition: {0:s} in file: {1:s}').format(
                    artifact_definition.name, filename))

          if source.type_indicator in (
              definitions.TYPE_INDICATOR_DIRECTORY,
              definitions.TYPE_INDICATOR_FILE, definitions.TYPE_INDICATOR_PATH):

            if (definitions.SUPPORTED_OS_DARWIN in source.supported_os or (
                artifact_definition_supports_macos and
                not source.supported_os)):
              if source.separator != '/':
                logging.warning((
                    'Use of unsupported path segment separator in artifact '
                    'definition: {0:s} in file: {1:s}').format(
                        artifact_definition.name, filename))

              macos_paths.extend(source.paths)

            elif (artifact_definition_supports_windows or
                  definitions.SUPPORTED_OS_WINDOWS in source.supported_os):
              for path in source.paths:
                if not self._CheckWindowsPath(
                    filename, artifact_definition, source, path):
                  result = False

            else:
              for path in source.paths:
                if not self._CheckPath(
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
              if not self._CheckWindowsRegistryKeyPath(
                  filename, artifact_definition, key_path):
                result = False

          elif source.type_indicator == (
              definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE):

            for key_value_pair in source.key_value_pairs:
              if not self._CheckWindowsRegistryKeyPath(
                  filename, artifact_definition, key_value_pair['key']):
                result = False

        if macos_paths:
          if not self._CheckMacOSPaths(
              filename, artifact_definition, macos_paths):
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
      'definitions', nargs='?', action='store', metavar='PATH', default=None,
      help=('path of the file or directory that contains the artifact '
            'definitions.'))

  options = args_parser.parse_args()

  if not options.definitions:
    print('Source value is missing.')
    print('')
    args_parser.print_help()
    print('')
    return False

  if not os.path.exists(options.definitions):
    print('No such file or directory: {0:s}'.format(options.definitions))
    print('')
    return False

  validator = ArtifactDefinitionsValidator()

  if os.path.isdir(options.definitions):
    print('Validating definitions in: {0:s}/*.yaml'.format(options.definitions))
    result = validator.CheckDirectory(options.definitions)

  elif os.path.isfile(options.definitions):
    print('Validating definitions in: {0:s}'.format(options.definitions))
    result = validator.CheckFile(options.definitions)

  if not result:
    print('FAILURE')
    return False

  print('SUCCESS')
  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
