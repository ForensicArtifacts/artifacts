#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tool to validate artifact definitions."""

from __future__ import print_function
from __future__ import unicode_literals
import argparse
import logging
import os
import sys

from artifacts import errors
from artifacts import reader
from artifacts import registry
from artifacts import source_type


class ArtifactDefinitionsValidator(object):
  """Class to define an artifact definitions validator."""

  def __init__(self):
    """Initializes the artifact definitions validator object."""
    super(ArtifactDefinitionsValidator, self).__init__()
    self._artifact_registry = registry.ArtifactDefinitionsRegistry()
    self.defined_artifact_names = set()
    self.artifact_name_references = set()

  def CheckFile(self, filename):
    """Validates the artifacts definition in a specific file.

    Args:
      filename: the filename of the artifacts definition file.
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

        self.defined_artifact_names.add(artifact_definition.name)
        for source in artifact_definition.sources:
          if isinstance(source, source_type.ArtifactSourceType):
            self.artifact_name_references.update(source.names)

    except errors.FormatError as exception:
      logging.warning(
          u'Unable to validate file: {0:s} with error: {1:s}'.format(
              filename, exception))
      result = False

    return result


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
