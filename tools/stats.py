#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Report statistics about the artifact collection."""

import sys
import time

from artifacts import definitions
from artifacts import reader


class ArtifactStatistics(object):
  """Generate and print statistics about artifact definitions."""

  def __init__(self):
    """Initializes artifact statistics."""
    super(ArtifactStatistics, self).__init__()
    self._os_counts = {}
    self._path_count = 0
    self._reg_key_count = 0
    self._source_type_counts = {}
    self._total_count = 0

  def _PrintDictAsTable(self, title, src_dict):
    """Prints a table of artifact definitions.

    Args:
      title (str): title of the table.
      src_dict (dict[str, ArtifactDefinition]): artifact definitions by name.
    """
    print('### {0:s}'.format(title))
    print('')
    print('Identifier | Number')
    print('--- | ---')

    for key, value in sorted(src_dict.items()):
      print('{0:s} | {1!s}'.format(key, value))

    print('')

  def PrintOSTable(self):
    """Prints a table of artifact definitions by operating system."""
    self._PrintDictAsTable('Operating systems', self._os_counts)

  def PrintSourceTypeTable(self):
    """Prints a table of artifact definitions by source type."""
    self._PrintDictAsTable(
        'Artifact definition source types', self._source_type_counts)

  def PrintSummaryTable(self):
    """Prints a summary table."""
    date_time_string = time.strftime('%Y-%m-%d')

    print("""Status of the repository as of {0:s}

Description | Number
--- | ---
Number of artifact definitions: | {1:d}
Number of file paths: | {2:d}
Number of Windows Registry key paths: | {3:d}
""".format(
    date_time_string, self._total_count, self._path_count, self._reg_key_count))

  def BuildStats(self):
    """Builds the statistics."""
    artifact_reader = reader.YamlArtifactsReader()
    self._os_counts = {}
    self._path_count = 0
    self._reg_key_count = 0
    self._source_type_counts = {}
    self._total_count = 0

    for artifact_definition in artifact_reader.ReadDirectory('data'):
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
    print("""## Statistics

The artifact definitions can be found in the [data directory]({0:s})
and the format is described in detail in the [Style Guide]({1:s}).
""".format('https://github.com/ForensicArtifacts/artifacts/tree/main/data',
           ('https://artifacts.readthedocs.io/en/latest/sources/'
            'Format-specification.html')))

    self.BuildStats()
    self.PrintSummaryTable()
    self.PrintSourceTypeTable()
    self.PrintOSTable()


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
