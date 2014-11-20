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
"""The artifact reader objects."""

import abc

from artifacts import artifact
from artifacts import definitions
from artifacts import errors


class ArtifactsReader(object):
  """Class that implements the artifacts reader interface."""

  @abc.abstractmethod
  def Read(self, file_object):
    """Reads artifact definitions.

    Args:
      file_object: the file-like object to read from.
 
    Yields:
      Artifact definitions (instances of ArtifactDefinition).
    """


class YamlArtifactsReader(ArtifactsReader):
  """Class that implements the YAML artifacts reader."""

  def _ReadArtifactDefinition(self, yaml_definition):
    """Reads an artifact definition.

    Args:
      yaml_definition: the YAML artifact definition.
 
    Returns:
      An artifact definition (instance of ArtifactDefinition).

    Raises:
      FormatError: if the format of the YAML artifact definition is incorrect.
      ValueError: if the YAML artifact definition is invalid.
    """
    if not yaml_definition:
      raise ValueError(u'Invalid YAML definition.')

    name = yaml_definition.get('name', None)
    if not name:
      raise errors.FormatError(u'Invalid artifact definition missing name.')

    description = yaml_definition.get('doc', None)
    artifact_definition = artifact.ArtifactDefinition(
        name, description=description)

    for collector in yaml_definition.get('collectors', []):
      type_indicator = collector.get('type', None)
      if not type_indicator:
        errors.FormatError(
            u'Invalid artifact definition collector missing type.')

    artifact_definition.conditions = yaml_definition.get('conditions', None)
    artifact_definition.labels = yaml_definition.get('labels', None)
    artifact_definition.supported_os = yaml_definition.get('supported_os', None)
    artifact_definition.urls = yaml_definition.get('urls', None)

    return artifact_definition

  def Read(self, file_object):
    """Reads artifact definitions.

    Args:
      file_object: the file-like object to read from.
 
    Yields:
      Artifact definitions (instances of ArtifactDefinition).
    """
    # TODO: add try, except?
    yaml_generator = yaml.safe_load_all(file_object)

    for yaml_definition in yaml_generator:
      yield self._ReadArtifactDefinition(yaml_definition)
