#!/usr/bin/python
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
  """Class to define an artifact definitions validator."""

  def __init__(self):
    """Initializes the artifact definitions validator object."""
    super(ArtifactDefinitionsValidator, self).__init__()
    self._artifact_name_references = set()
    self._artifact_registry = registry.ArtifactDefinitionsRegistry()
    self._artifact_registry_key_paths = set()
    self._defined_artifact_names = set()

  def _CheckDuplicateRegistryKeyPaths(
      self, filename, artifact_definition, source):
    """Checks if Registry key paths are not already defined by other artifacts.

    Args:
      filename: the filename of the artifacts definition file.
      artifact_definition: the artifact definition (instance of
                           ArtifactDefinition).
      source: the source definition (instance of SourceType).

    Returns:
      A boolean indicating the Registry key paths defined by the source type
      are not already used in other artifacts.
    """
    result = True
    intersection = self._artifact_registry_key_paths.intersection(
        set(source.keys))
    if intersection:
      duplicate_key_paths = u'\n'.join(intersection)
      logging.warning((
          u'Artifact definition: {0} in file: {1} has duplicate '
          u'Registry key paths:\n{2}').format(
              artifact_definition.name, filename, duplicate_key_paths))
      result = False

    self._artifact_registry_key_paths.update(source.keys)
    return result

  def CheckFile(self, filename):
    """Validates the artifacts definition in a specific file.

    Args:
      filename: the filename of the artifacts definition file.

    Returns:
      A boolean indicating the file contains valid artifacts definitions.
    """
    result = True
    artifact_reader = reader.YamlArtifactsReader()

    try:
      for artifact_definition in artifact_reader.ReadFile(filename):
        try:
          self._artifact_registry.RegisterDefinition(artifact_definition)
        except KeyError:
          logging.warning(
              u'Duplicate artifact definition: {0} in file: {1}'.format(
                  artifact_definition.name, filename))
          result = False

        self._defined_artifact_names.add(artifact_definition.name)
        for source in artifact_definition.sources:
          if source.type_indicator == definitions.TYPE_INDICATOR_ARTIFACT_GROUP:
            self._artifact_name_references.update(source.names)

          elif source.type_indicator in (
              definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY):
            if not self._CheckDuplicateRegistryKeyPaths(
                filename, artifact_definition, source):
              result = False

    except errors.FormatError as exception:
      logging.warning(
          u'Unable to validate file: {0} with error: {1}'.format(
              filename, exception))
      result = False

    return result

  def MissingArtifacts(self):
    """Determines the names of undefined artifacts used by artifact groups.

    Returns:
      A set of the missing artifacts names.
    """
    return self._artifact_name_references - self._defined_artifact_names


def Main():
  """The main program function.

  Returns:
    A boolean containing True if successful or False if not.
  """
  args_parser = argparse.ArgumentParser(description=(
      'Validates an artifact definitions file.'))

  args_parser.add_argument(
      'filename', nargs='?', action='store', metavar='artifacts.yaml',
      default=None, help=('path of the file that contains the artifact '
                          'definitions.'))

  options = args_parser.parse_args()

  if not options.filename:
    print('Source value is missing.')
    print('')
    args_parser.print_help()
    print('')
    return False

  if not os.path.isfile(options.filename):
    print('No such file: {0}'.format(options.filename))
    print('')
    return False

  print('Validating: {0}'.format(options.filename))
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
