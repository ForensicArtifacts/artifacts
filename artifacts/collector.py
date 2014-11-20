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
"""The collector definition objects."""

from artifacts import definitions


class CollectorDefinition(object):
  """Class that implements the collector definition interface."""

  TYPE_INDICATOR = None

  def __init__(self, **kwargs):
    """Initializes the collector definition object.

    Args:
      kwargs: a dictionary of keyword arguments dependending on
              the collector type.

    Raises:
      ValueError: when there are unused keyword arguments.
    """
    if kwargs:
      raise ValueError(u'Unused keyword arguments.')

    super(CollectorDefinition, self).__init__()

  @property
  def type_indicator(self):
    """The type indicator."""
    type_indicator = getattr(self, 'TYPE_INDICATOR', None)
    if type_indicator is None:
      raise NotImplementedError(
          u'Invalid path specification missing type indicator.')
    return type_indicator


class FileCollectorDefinition(CollectorDefinition):
  """Class that implements the file collector definition."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_FILE

  def __init__(self, path_list=None, **kwargs):
    """Initializes the artifact definition source type object.

    Args:
      path_list: optional list of path strings. The default is None.

    Raises:
      ValueError: when path_list is not set.
    """
    if not locations:
      raise ValueError(u'Missing path_list value.')

    super(FileCollectorDefinition, self).__init__(**kwargs)
    self.path_list = path_list
