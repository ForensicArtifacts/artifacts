#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tool to validate artifact definitions."""

import argparse
import logging
import os
import sys

from artifacts import errors
from artifacts import reader


class Validator(object):
  """Class to define an artifact definitions validator."""

  def Run(self, filename):
    """Runs the validator on an artifacts definition file.

    Args:
      filename: the filename of the artifacts definition file.
    """
    result = True
    with open(filename, 'rb') as file_object:
      artifact_reader = reader.YamlArtifactsReader()

      try:
        for _ in artifact_reader.Read(file_object):
          pass

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
      'source', nargs='?', action='store', metavar='artifacts.yaml',
      default=None, help=('path of the file that contains the artifact '
                          'definitions.'))

  options = args_parser.parse_args()

  if not options.source:
    print u'Source value is missing.'
    print u''
    args_parser.print_help()
    print u''
    return False

  if not os.path.isfile(options.source):
    print u'Invalid source.'
    print u''
    return False

  print u'Validating: {0:s}'.format(options.source)
  validator = Validator()
  if not validator.Run(options.source):
    print u'FAILURE'
    return False

  print u'SUCCESS'
  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
