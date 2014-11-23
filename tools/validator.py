#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 The ForensicArtifacts.com Artifact Repository project.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tool to validate artifact definitions."""

import argparse
import logging
import os
import sys

from artifacts import definitions
from artifacts import reader


class Validator(object):
  """Class to define an artifact definitions validator."""

  def _CheckArtifactDefinition(self, artifact_definition):
    """Checks an artifact definition.

    Args:
      artifact_definition: the artifact definition object (instance of
                           ArtifactDefinition).

    Returns:
      A boolean value indicating the artifact definition is valid or not.
    """
    result = True

    if not artifact_definition.description:
      logging.warning(
          u'Artifact definition: {0:s} missing description.'.format(
              artifact_definition.name))
      result = False

    if not artifact_definition.collectors:
      logging.warning(
          u'Artifact definition: {0:s} missing collectors.'.format(
              artifact_definition.name))
      result = False

    else:
      for collector in artifact_definition.collectors:
        if not self._CheckCollectorDefinition(
            artifact_definition.name, collector):
          result = False

    for operating_system in artifact_definition.supported_os:
      if operating_system not in definitions.SUPPORTED_OS:
        logging.warning((
            u'Artifact definition: {0:s} supported operating system: {1:s} '
            u'not defined.').format(artifact_definition.name, operating_system))

    # TODO: check conditions.

    for label in artifact_definition.labels:
      if label not in definitions.LABELS:
        logging.warning(
            u'Artifact definition: {0:s} label: {1:s} not defined.'.format(
                artifact_definition.name, label))

    return result

  def _CheckCollectorDefinition(
      self, artifact_definition_name, collector_definition):
    """Checks a collector definition.

    Args:
      artifact_definition_name: string containing the name of the artifact
                                defintion.
      collector_definition: the collector definition object (instance of
                            CollectorDefinition).

    Returns:
      A boolean value indicating the collector definition is valid or not.
    """
    type_indicator = collector_definition.type_indicator

    result = True
    if type_indicator in definitions.TYPE_INDICATOR_ARTIFACT:
      if not collector_definition.artifact_list:
        logging.warning((
            u'Artifact definition: {0:s} artifact collector definition missing '
            u'artifiact list.').format(artifact_definition_name))
        result = False

    elif type_indicator == definitions.TYPE_INDICATOR_FILE:
      if not collector_definition.path_list:
        logging.warning((
            u'Artifact definition: {0:s} file collector definition missing '
            u'path list.').format(artifact_definition_name))
        result = False

    elif type_indicator == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY:
      if not collector_definition.path_list:
        logging.warning((
            u'Artifact definition: {0:s} Windows Registry key collector '
            u'definition missing path list.').format(artifact_definition_name))
        result = False

    elif type_indicator == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE:
      if not collector_definition.path_list:
        logging.warning((
            u'Artifact definition: {0:s} Windows Registry value collector '
            u'definition missing path list.').format(artifact_definition_name))
        result = False

    elif type_indicator == definitions.TYPE_INDICATOR_WMI_QUERY:
      if not collector_definition.query:
        logging.warning((
            u'Artifact definition: {0:s} WMI query collector definition '
            u'missing query.').format(artifact_definition_name))
        result = False

    else: 
      logging.warning((
          u'Artifact definition: {0:s} unsupported collector definition type: '
          u'{1:s}.').format(artifact_definition_name, type_indicator))
      result = False

    for operating_system in collector_definition.supported_os:
      if operating_system not in definitions.SUPPORTED_OS:
        logging.warning((
            u'Artifact definition: {0:s} collector definition: {1:s} supported '
            u'operating system: {2:s} not defined.').format(
                artifact_definition_name, type_indicator, operating_system))

    # TODO: check conditions.

    return result

  def Run(self, filename):
    """Runs the validator on an artifacts definition file.

    Args:
      filename: the filename of the artifacts definition file.
    """
    with open(filename, 'rb') as file_object:
      try:
        artifact_reader = reader.YamlArtifactsReader()
      except errors.FormatError as exception:
        logging.warning(
            u'Unable to read artifacts definitions with error: {0:s}'.format(
               exception))
        return False

      result = True
      for artifact_definition in artifact_reader.Read(file_object):
        result = self._CheckArtifactDefinition(artifact_definition)
        if not result:
          break

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
