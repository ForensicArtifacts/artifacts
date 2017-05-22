#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Report statistics about the artifact collection."""

from __future__ import print_function
import time

from artifacts import definitions
from artifacts import reader


class ArtifactStatistics(object):
  """Generate and print statistics about artifact files."""

  def __init__(self):
    """Initializes artifact statistics."""
    super(ArtifactStatistics, self).__init__()
    self.label_counts = {}
    self.os_counts = {}
    self.path_count = 0
    self.reg_key_count = 0
    self.source_type_counts = {}
    self.total_count = 0

  def _PrintDictAsTable(self, src_dict):
    """Prints a table of artifact definitions.

    Args:
      src_dict (dict[str, ArtifactDefinition]): artifact definitions by name.
    """
    key_list = list(src_dict.keys())
    key_list.sort()

    print('|', end='')
    for key in key_list:
      print(' {0} |'.format(key), end='')
    print('')

    print('|', end='')
    for key in key_list:
      print(' :---: |', end='')
    print('')

    print('|', end='')
    for key in key_list:
      print(' {0} |'.format(src_dict[key]), end='')
    print('\n')

  def PrintOSTable(self):
    """Prints a table of artifact definitions by operating system."""
    print('**Artifacts by OS**\n')
    self._PrintDictAsTable(self.os_counts)

  def PrintLabelTable(self):
    """Prints a table of artifact definitions by label."""
    print('**Artifacts by label**\n')
    self._PrintDictAsTable(self.label_counts)

  def PrintSourceTypeTable(self):
    """Prints a table of artifact definitions by source type."""
    print('**Artifacts by type**\n')
    self._PrintDictAsTable(self.source_type_counts)

  def PrintSummaryTable(self):
    """Prints a summary table."""
    print("""

As of {0} the repository contains:

| **File paths covered** | **{1}** |
| :------------------ | ------: |
| **Registry keys covered** | **{2}** |
| **Total artifacts** | **{3}** |
""".format(
    time.strftime('%Y-%m-%d'), self.path_count, self.reg_key_count,
    self.total_count))

  def BuildStats(self):
    """Builds the statistics."""
    artifact_reader = reader.YamlArtifactsReader()
    self.label_counts = {}
    self.os_counts = {}
    self.path_count = 0
    self.reg_key_count = 0
    self.source_type_counts = {}
    self.total_count = 0

    for artifact_definition in artifact_reader.ReadDirectory('data'):
      if hasattr(artifact_definition, 'labels'):
        for label in artifact_definition.labels:
          self.label_counts[label] = self.label_counts.get(label, 0) + 1

      for source in artifact_definition.sources:
        self.total_count += 1
        source_type = source.type_indicator
        self.source_type_counts[source_type] = self.source_type_counts.get(
            source_type, 0) + 1

        if source_type == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY:
          self.reg_key_count += len(source.keys)
        if source_type == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE:
          self.reg_key_count += len(source.key_value_pairs)
        if (source_type == definitions.TYPE_INDICATOR_FILE or
            source_type == definitions.TYPE_INDICATOR_DIRECTORY):
          self.path_count += len(source.paths)

        os_list = source.supported_os
        for os_str in os_list:
          self.os_counts[os_str] = self.os_counts.get(os_str, 0) + 1

  def PrintStats(self):
    """Build stats and print in MarkDown format."""
    self.BuildStats()
    self.PrintSummaryTable()
    self.PrintSourceTypeTable()
    self.PrintOSTable()
    self.PrintLabelTable()


def main():
  """The main function."""
  statsbuilder = ArtifactStatistics()
  statsbuilder.PrintStats()


if __name__ == '__main__':
  main()
