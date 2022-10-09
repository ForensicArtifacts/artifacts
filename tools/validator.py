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
          f'Unuspported globstar with prefix: {path_segment:s} for path: '
          f'{path:s} defined by artifact definition: '
          f'{artifact_definition.name:s} in file: {filename:s}'))
      return False

    if len(path_segment) > 2:
      try:
        recursion_depth = int(path_segment[2:], 10)
      except (TypeError, ValueError):
        logging.warning((
            f'Unuspported globstar with suffix: {path_segment:s} for path: '
            f'{path:s} defined by artifact definition: '
            f'{artifact_definition.name:s} in file: {filename:s}'))
        return False

      if recursion_depth <= 0 or recursion_depth > 10:
        logging.warning((
            f'Globstar with unsupported recursion depth: {path_segment:s} for '
            f'path: {path:s} defined by artifact definition: '
            f'{artifact_definition.name:s} in file: {filename:s}'))
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
            f'Empty path defined by artifact definition: '
            f'{artifact_definition.name:s} in file: {filename:s}'))
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
              f'Unsupported private path: {path:s} defined by artifact '
              f'definition: {artifact_definition.name:s} in file: '
              f'{filename:s}'))
          result = False

      has_globstar = False
      for path_segment in path_segments:
        if '**' in path_segment:
          if has_globstar:
            logging.warning((
                f'Unsupported path: {path:s} with multiple globstars defined '
                f'by artifact definition: {artifact_definition.name:s} in '
                f'file: {filename:s}'))
            result = False
            break

          has_globstar = True
          if not self._CheckGlobstarInPathSegment(
              filename, artifact_definition, path, path_segment):
            result = False

      if has_globstar and path.endswith('/'):
        logging.warning((
            f'Unsupported path: {path:s} with globstar and trailing path '
            f'separator defined by artifact definition: '
            f'{artifact_definition.name:s} in file: {filename:s}'))
        result = False

    for private_path in paths_with_private:
      symbolic_link = private_path[8:]
      if symbolic_link not in paths_with_symbolic_link_to_private:
        logging.warning((
            f'Missing symbolic link: {symbolic_link:s} for path: '
            f'{private_path:s} defined by artifact definition: '
            f'{artifact_definition.name:s} in file: {filename:s}'))
        result = False

    for path in paths_with_symbolic_link_to_private:
      private_path = f'/private{path:s}'
      if private_path not in paths_with_private:
        logging.warning((
            f'Missing path: {private_path:s} for symbolic link: {path:s} '
            f'defined by artifact definition: {artifact_definition.name:s} in '
            f'file: {filename:s}'))
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
              f'Unsupported path: {path:s} with multiple globstars defined by '
              f'artifact definition: {artifact_definition.name:s} in file: '
              f'{filename:s}'))
          result = False
          break

        has_globstar = True
        if not self._CheckGlobstarInPathSegment(
            filename, artifact_definition, path, path_segment):
          result = False

    if has_globstar and path.endswith(source.separator):
      logging.warning((
          f'Unsupported path: {path:s} with globstar and trailing path '
          f'separator defined by artifact definition: '
          f'{artifact_definition.name:s} in file: {filename:s}'))
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
          f'Incorrect path separator: {source.separator:s} in path: {path:s} '
          f'defined by artifact definition: {artifact_definition.name:s} in '
          f'file: {filename:s}'))
      result = False

    if source.separator != '\\':
      return result

    path_lower = path.lower()
    path_segments = path_lower.split(source.separator)
    if not path_segments:
      logging.warning((
          f'Empty path defined by artifact definition: '
          f'{artifact_definition.name:s} in file: {filename:s}'))
      result = False

    elif path_segments[0].startswith('%%users.') and path_segments[0] not in (
        '%%users.appdata%%', '%%users.homedir%%', '%%users.localappdata%%',
        '%%users.temp%%', '%%users.username%%', '%%users.userprofile%%'):
      logging.warning((
          f'Unsupported "{path_segments[0]:s}" in path: {path:s} defined by '
          f'artifact definition: {artifact_definition.name:s} in file: '
          f'{filename:s}'))
      result = False

    elif path_segments[0] == '%%users.homedir%%':
      logging.warning((
          f'Replace "%%users.homedir%%" by "%%users.userprofile%%" in path: '
          f'{path:s} defined by artifact definition: '
          f'{artifact_definition.name:s} in file: {filename:s}'))
      result = False

    elif path_lower.startswith('%%users.userprofile%%\\appdata\\local\\'):
      logging.warning((
          f'Replace "%%users.userprofile%%\\AppData\\Local" by '
          f'"%%users.localappdata%%" in path: {path:s} defined by artifact '
          f'definition: {artifact_definition.name:s} in file: {filename:s}'))
      result = False

    elif path_lower.startswith('%%users.userprofile%%\\appdata\\roaming\\'):
      logging.warning((
          f'Replace "%%users.userprofile%%\\AppData\\Roaming" by '
          f'"%%users.appdata%%" in path: {path:s} defined by artifact '
          f'definition: {artifact_definition.name:s} in file: {filename:s}'))
      result = False

    elif path_lower.startswith('%%users.userprofile%%\\application data\\'):
      logging.warning((
          f'Replace "%%users.userprofile%%\\Application Data" by '
          f'"%%users.appdata%%" in path: {path:s} defined by artifact '
          f'definition: {artifact_definition.name:s} in file: {filename:s}'))
      result = False

    elif path_lower.startswith(
        '%%users.userprofile%%\\local settings\\application data\\'):
      logging.warning((
          f'Replace "%%users.userprofile%%\\Local Settings\\Application Data" '
          f'by "%%users.localappdata%%" in path: {path:s} defined by artifact '
          f'definition: {artifact_definition.name:s} in file: {filename:s}'))
      result = False

    has_globstar = False
    for path_segment in path_segments:
      if path_segment.startswith('%%') and path_segment.endswith('%%'):
        if (path_segment.startswith('%%environ_') and
            path_segment not in self._SUPPORTED_WINDOWS_ENVIRONMENT_VARIABLES):
          result = False
          logging.warning((
              f'Artifact definition: {artifact_definition.name:s} in file: '
              f'{filename:s} contains Windows path that contains an '
              f'unuspported environment variable: "{path_segment:s}".'))

        elif (path_segment.startswith('%%users.') and
              path_segment not in self._SUPPORTED_WINDOWS_USERS_VARIABLES):
          result = False
          logging.warning((
              f'Artifact definition: {artifact_definition.name:s} in file: '
              f'{filename:s} contains Windows path that contains an '
              f'unsupported users variable: "{path_segment:s}". '))

      elif '**' in path_segment:
        if has_globstar:
          logging.warning((
              f'Unsupported path: {path:s} with multiple globstars defined by '
              f'artifact definition: {artifact_definition.name:s} in file: '
              f'{filename:s}'))
          result = False
          break

        has_globstar = True
        if not self._CheckGlobstarInPathSegment(
            filename, artifact_definition, path, path_segment):
          result = False

    if has_globstar and path.endswith(source.separator):
      logging.warning((
          f'Unsupported path: {path:s} with globstar and trailing path '
          f'separator defined by artifact definition: '
          f'{artifact_definition.name:s} in file: {filename:s}'))
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
          f'Artifact definition: {artifact_definition.name:s} in file: '
          f'{filename:s} contains Windows Registry key path that starts with '
          f'%%CURRENT_CONTROL_SET%%. Replace %%CURRENT_CONTROL_SET%% with '
          f'HKEY_LOCAL_MACHINE\\System\\CurrentControlSet'))

    for segment_index, key_path_segment in enumerate(key_path_segments):
      if key_path_segment.startswith('%%') and key_path_segment.endswith('%%'):
        if (segment_index == 1 and key_path_segment == '%%users.sid%%' and
            key_path_segments[0] == 'hkey_users'):
          continue

        if key_path_segment.startswith('%%environ_'):
          result = False
          logging.warning((
              f'Artifact definition: {artifact_definition.name:s} in file: '
              f'{filename:s} contains Windows Registry key path that contains '
              f'an environment variable: "{key_path_segment:s}". Usage of '
              f'environment variables in key paths is not encouraged at this '
              f'time.'))

        elif key_path_segment.startswith('%%users.'):
          result = False
          logging.warning((
              f'Artifact definition: {artifact_definition.name:s} in file: '
              f'{filename:s} contains Windows Registry key path that contains '
              f'a users variable: "{key_path_segment:s}". Usage of users '
              f'variables in key paths, except for '
              f'"HKEY_USERS\\%%users.sid%%", is not encouraged at this time.'))

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
          f'Artifact definition: {artifact_definition.name:s} in file: '
          f'{filename:s} has duplicate Registry key paths:\n'
          f'{duplicate_key_paths:s}'))
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
          logging.warning((
              f'Duplicate artifact definition: {artifact_definition.name:s} in '
              f'file: {filename:s}'))
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
                f'Use of deprecated source type: DIRECTORY in artifact '
                f'definition: {artifact_definition.name:s} in file: '
                f'{filename:s}'))

          if source.type_indicator in (
              definitions.TYPE_INDICATOR_DIRECTORY,
              definitions.TYPE_INDICATOR_FILE, definitions.TYPE_INDICATOR_PATH):

            if (definitions.SUPPORTED_OS_DARWIN in source.supported_os or (
                artifact_definition_supports_macos and
                not source.supported_os)):
              if source.separator != '/':
                logging.warning((
                    f'Use of unsupported path segment separator in artifact '
                    f'definition: {artifact_definition.name:s} in file: '
                    f'{filename:s}'))

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
          f'Unable to validate file: {filename:s} with error: {exception!s}')
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
    print(f'No such file or directory: {options.definitions:s}')
    print('')
    return False

  validator = ArtifactDefinitionsValidator()

  if os.path.isdir(options.definitions):
    print(f'Validating definitions in: {options.definitions:s}/*.yaml')
    result = validator.CheckDirectory(options.definitions)

  elif os.path.isfile(options.definitions):
    print(f'Validating definitions in: {options.definitions:s}')
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
