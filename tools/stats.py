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
    print(f'### {title:s}')
    print('')
    print('Identifier | Number')
    print('--- | ---')

    for key, value in sorted(src_dict.items()):
      print(f'{key:s} | {value!s}')

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

    print(f"""Status of the repository as of {date_time_string:s}

Description | Number
--- | ---
Number of artifact definitions: | {self._total_count:d}
Number of file paths: | {self._path_count:d}
Number of Windows Registry key paths: | {self._reg_key_count:d}
""")

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
    data_directory_url = (
        'https://github.com/ForensicArtifacts/artifacts/tree/main/data')

    style_guide_url = (
        'https://artifacts.readthedocs.io/en/latest/sources/'
        'Format-specification.html')

    print(f"""## Statistics

The artifact definitions can be found in the
[data directory]({data_directory_url:s}) and the format is described in detail
in the [Style Guide]({style_guide_url:s}).
""")

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
