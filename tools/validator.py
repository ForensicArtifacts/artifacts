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

    if key_path.startswith(u'%%CURRENT_CONTROL_SET%%'):
      result = False
      logging.warning((
          u'Artifact definition: {0:s} in file: {1:s} contains Windows '
          u'Registry key path that starts with '
          u'%%CURRENT_CONTROL_SET%%. Replace %%CURRENT_CONTROL_SET%% with '
          u'HKEY_LOCAL_MACHINE\\System\\CurrentControlSet').format(
              artifact_definition.name, filename))

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
      duplicate_key_paths = u'\n'.join(intersection)
      logging.warning((
          u'Artifact definition: {0:s} in file: {1:s} has duplicate '
          u'Registry key paths:\n{2:s}').format(
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
              u'Duplicate artifact definition: {0:s} in file: {1:s}'.format(
                  artifact_definition.name, filename))
          result = False

        for source in artifact_definition.sources:
          if source.type_indicator == (
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
                  filename, artifact_definition, key_value_pair[u'key']):
                result = False

    except errors.FormatError as exception:
      logging.warning(
          u'Unable to validate file: {0:s} with error: {1!s}'.format(
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
