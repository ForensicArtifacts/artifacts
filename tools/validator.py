#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tool to validate artifact definitions."""

import argparse
import logging
import os
import sys

from artifacts import errors
from artifacts import reader
from artifacts import registry


class ArtifactDefinitionsValidator(object):
  """Class to define an artifact definitions validator."""

  def __init__(self):
    """Initializes the artifact definitions validator object."""
    super(ArtifactDefinitionsValidator, self).__init__()
    self._artifact_registry = registry.ArtifactDefinitionsRegistry()

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

    except errors.FormatError as exception:
      logging.warning(exception.message)
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
    print u'Source value is missing.'
    print u''
    args_parser.print_help()
    print u''
    return False

  if not os.path.isfile(options.filename):
    print u'No such file: {0:s}'.format(options.filename)
    print u''
    return False

  print u'Validating: {0:s}'.format(options.filename)
  validator = ArtifactDefinitionsValidator()
  if not validator.CheckFile(options.filename):
    print u'FAILURE'
    return False

  print u'SUCCESS'
  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
