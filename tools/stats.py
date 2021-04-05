#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Report statistics about the artifact collection."""

from __future__ import print_function
from __future__ import unicode_literals

import sys
import time

from artifacts import definitions
from artifacts import reader


class ArtifactStatistics(object):
  """Generate and print statistics about artifact definitions."""

  def __init__(self):
    """Initializes artifact statistics."""
    super(ArtifactStatistics, self).__init__()
    self._label_counts = {}
    self._os_counts = {}
    self._path_count = 0
    self._reg_key_count = 0
    self._source_type_counts = {}
    self._total_count = 0

  def _PrintDictAsTable(self, src_dict):
    """Prints a table of artifact definitions.

    Args:
      src_dict (dict[str, ArtifactDefinition]): artifact definitions by name.
    """
    print('<table>')

    for key, value in sorted(src_dict.items()):
      print('  <tr>')
      print('    <th nowrap style="text-align:left;vertical-align:top">')
      print('      {0:s}</th>'.format(key))
      print('    <td>{0!s}</td>'.format(value))
      print('  </tr>')

    print('</table>')
    print('')

  def PrintOSTable(self):
    """Prints a table of artifact definitions by operating system."""
    print('**Operating systems**\n')
    self._PrintDictAsTable(self._os_counts)

  def PrintLabelTable(self):
    """Prints a table of artifact definitions by label."""
    print('**Labels**\n')
    self._PrintDictAsTable(self._label_counts)

  def PrintSourceTypeTable(self):
    """Prints a table of artifact definitions by source type."""
    print('**Artifact definition source types**\n')
    self._PrintDictAsTable(self._source_type_counts)

  def PrintSummaryTable(self):
    """Prints a summary table."""
    date_time_string = time.strftime('%Y-%m-%d')

    print("""
**Status of the repository as of {0:s}**

<table>
  <tr>
    <th nowrap style="text-align:left;vertical-align:top">
      Number of artifact definitions:</th>
    <td>{1:d}</td>
  </tr>
  <tr>
    <th nowrap style="text-align:left;vertical-align:top">
      Number of file paths:</th>
    <td>{2:d}</td>
  </tr>
  <tr>
    <th nowrap style="text-align:left;vertical-align:top">
      Number of Windows Registry key paths:</th>
    <td>{3:d}</td>
  </tr>
</table>
""".format(
    date_time_string, self._total_count, self._path_count, self._reg_key_count))

  def BuildStats(self):
    """Builds the statistics."""
    artifact_reader = reader.YamlArtifactsReader()
    self._label_counts = {}
    self._os_counts = {}
    self._path_count = 0
    self._reg_key_count = 0
    self._source_type_counts = {}
    self._total_count = 0

    for artifact_definition in artifact_reader.ReadDirectory('data'):
      if hasattr(artifact_definition, 'labels'):
        for label in artifact_definition.labels:
          self._label_counts[label] = self._label_counts.get(label, 0) + 1

      for source in artifact_definition.sources:
        self._total_count += 1
        source_type = source.type_indicator
        self._source_type_counts[source_type] = self._source_type_counts.get(
            source_type, 0) + 1

        if source_type == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY:
          self._reg_key_count += len(source.keys)
        elif source_type == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE:
          self._reg_key_count += len(source.key_value_pairs)
        elif source_type in (definitions.TYPE_INDICATOR_FILE,
                             definitions.TYPE_INDICATOR_DIRECTORY):
          self._path_count += len(source.paths)

        os_list = source.supported_os
        for os_str in os_list:
          self._os_counts[os_str] = self._os_counts.get(os_str, 0) + 1

  def PrintStats(self):
    """Build stats and print in MarkDown format."""
    self.BuildStats()
    self.PrintSummaryTable()
    self.PrintSourceTypeTable()
    self.PrintOSTable()
    self.PrintLabelTable()


def Main():
  """The main program function.

  Returns:
    bool: True if successful or False if not.
  """
  statsbuilder = ArtifactStatistics()
  statsbuilder.PrintStats()
  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
