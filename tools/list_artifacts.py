#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tool to list artifacts by operating system."""

import argparse
import csv
import os
import sys
from typing import Any, Dict, Iterator

from artifacts import definitions
from artifacts import reader
from artifacts import source_type


class ArtifactLister():
  """Generate a listing of artifact definitions for an operating system.

  Attributes:
    directory (str): the data directory of artifact definitions.
    target_os (str): the target operating system.
    split_paths (bool): split artifict definitions into separate entries when
       there are more than one path values.
  """

  def __init__(self, directory, target_os, split_paths=False):
    """Initializes an artifact lister.

    Args:
      directory: the data directory of artifact definitions.
      target_os: the target operating system.
      split_paths: split artifict definitions into separate entries when
         there are more than one path values.
    """
    self.directory = directory
    self.target_os = target_os
    self.split_paths = split_paths

  def _GenerateCommand(
      self, name: str, doc: str, source: source_type.CommandSourceType
  ) -> Iterator[Dict[str, Any]]:
    """Generates dictionaries from a Command artifact.

    Args:
      name: the name of the artifact
      doc: the documentation of the artifact
      source: the source artifact

    Yields:
      A dictionary of the artifact.
    """
    record = {
        'name': name, 'type': source.type_indicator, 'os': self.target_os,
        'cmd': source.cmd, 'args': ' '.join(source.args), 'doc': doc}
    yield record

  def _GenerateDirectory(
      self, name: str, doc: str, source: source_type.DirectorySourceType
  ) -> Iterator[Dict[str, Any]]:
    """Generates directories from a Directory artifact.

    Args:
      name: the name of the artifact
      doc: the documentation of the artifact
      source: the source artifact

    Yields:
      A dictionary of the artifact.
    """
    if self.split_paths:
      for path in source.paths:
        record = {
            'name': name, 'type': source.type_indicator, 'os': self.target_os,
            'path': path, 'doc': doc}
        yield record
    else:
      record = {
          'name': name, 'type': source.type_indicator, 'os': self.target_os,
          'path': source.paths, 'doc': doc}
      yield record

  def _GenerateFile(
      self, name: str, doc: str, source: source_type.FileSourceType
  ) -> Iterator[Dict[str, Any]]:
    """Generates directories from a File artifact.

    Args:
      name: the name of the artifact
      doc: the documentation of the artifact
      source: the source artifact

    Yields:
      A dictionary of the artifact.
    """
    if self.split_paths:
      for path in source.paths:
        record = {
            'name': name, 'type': source.type_indicator, 'os': self.target_os,
            'path': path, 'doc': doc}
        yield record
    else:
      record = {
          'name': name, 'type': source.type_indicator, 'os': self.target_os,
          'path': source.paths, 'doc': doc}
      yield record

  def _GeneratePath(
      self, name: str, doc: str, source: source_type.PathSourceType
  ) -> Iterator[Dict[str, Any]]:
    """Generates directories from a Path artifact.

    Args:
      name: the name of the artifact
      doc: the documentation of the artifact
      source: the source artifact

    Yields:
      A dictionary of the artifact.
    """
    if self.split_paths:
      for path in source.paths:
        record = {
            'name': name, 'type': source.type_indicator, 'os': self.target_os,
            'path': path, 'doc': doc}
        yield record
    else:
      record = {
          'name': name, 'type': source.type_indicator,
          'os': self.target_os, 'path': source.paths, 'doc': doc}
      yield record

  def _GenerateWindowsRegistryKey(
      self, name: str, doc: str,
      source: source_type.WindowsRegistryKeySourceType
  ) -> Iterator[Dict[str, Any]]:
    """Generates directories from a Windows Registry Key artifact.

    Args:
      name: the name of the artifact
      doc: the documentation of the artifact
      source: the source artifact

    Yields:
      A dictionary of the artifact.
    """
    for key in source.keys:
      record = {
          'name': name, 'type': source.type_indicator, 'os': self.target_os,
          'key': key, 'doc': doc}
      yield record

  def _GenerateWindowsRegistryValue(
      self, name: str, doc: str,
      source: source_type.WindowsRegistryValueSourceType
  ) -> Iterator[Dict[str, Any]]:
    """Generates directories from a Windows Registry Value artifact.

    Args:
      name: the name of the artifact
      doc: the documentation of the artifact
      source: the source artifact

    Yields:
      A dictionary of the artifact.
    """
    for key, value in source.key_value_pairs:
      record = {
          'name': name, 'type': source.type_indicator,
          'os': self.target_os, 'key': key, 'value': value, 'doc': doc}
      yield record

  def _GenerateWMIQuery(
      self, name: str, doc: str, source: source_type.WMIQuerySourceType
  ) -> Iterator[Dict[str, Any]]:
    """Generates directories from a WMI Query artifact.

    Args:
      name: the name of the artifact
      doc: the documentation of the artifact
      source: the source artifact

    Yields:
      A dictionary of the artifact.
    """
    record = {
        'name': name, 'type': source.type_indicator,
        'os': self.target_os, 'query': source.query,
        'base_object': source.base_object, 'doc': doc}
    yield record

  def _LoadArtifacts(self) -> Iterator[Dict[str, Any]]:
    """Loads artifact definitions and generates dictionary representations.

    Yields:
      A dictionary representing an artifact.
    """
    artifact_reader = reader.YamlArtifactsReader()

    for artifact_definition in artifact_reader.ReadDirectory(self.directory):
      name = artifact_definition.name
      doc = artifact_definition.description

      if self.target_os not in artifact_definition.supported_os:
        continue

      for source in artifact_definition.sources:
        supported_oses = source.supported_os
        if supported_oses and self.target_os not in supported_oses:
          continue

        if isinstance(source, source_type.CommandSourceType):
          yield from self._GenerateCommand(name, doc, source)
        elif isinstance(source, source_type.DirectorySourceType):
          yield from self._GenerateDirectory(name, doc, source)
        elif isinstance(source, source_type.FileSourceType):
          yield from self._GenerateFile(name, doc, source)
        elif isinstance(source, source_type.PathSourceType):
          yield from self._GeneratePath(name, doc, source)
        elif isinstance(source, source_type.WindowsRegistryKeySourceType):
          yield from self._GenerateWindowsRegistryKey(name, doc, source)
        elif isinstance(source, source_type.WindowsRegistryValueSourceType):
          yield from self._GenerateWindowsRegistryValue(name, doc, source)
        elif isinstance(source, source_type.WMIQuerySourceType):
          yield from self._GenerateWMIQuery(name, doc, source)

  def PrintArtifacts(self, show_docs=False):
    """Prints artifacts in a key-value list."""
    for artifact in sorted(self._LoadArtifacts(),
                           key=lambda artifact: artifact['name']):
      print('Name:       ', artifact['name'])
      print('Type:       ', artifact['type'])
      print('OS:         ', artifact['os'])
      if 'path' in artifact:
        print('Path:       ', artifact['path'])
      if 'key' in artifact:
        print('Key:        ', artifact['key'])
      if 'value' in artifact:
        print('Value:      ', artifact['value'])
      if 'query' in artifact:
        print('Query:      ', artifact['query'])
      if 'base_object' in artifact:
        print('Base Object:', artifact['base_object'])
      if 'cmd' in artifact:
        print('Command:    ', artifact['cmd'])
      if 'args' in artifact:
        print('Arguments:  ', artifact['args'])
      if show_docs:
        print('Docs:       ', artifact['doc'])
      print()

  def PrintJSONL(self):
    """Prints artifacts in a JSON-L format."""
    for artifact in self._LoadArtifacts():
      print(artifact)

  def PrintCSV(self):
    """Prints artifacts in a CSV format."""
    fieldnames = [
        'name', 'type', 'os', 'path', 'key', 'value', 'names', 'query',
        'base_object', 'cmd', 'args', 'doc']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    for artifact in self._LoadArtifacts():
      writer.writerow(artifact)


def Main():
  """The main program function.

  Returns:
    bool: True if successful or False if not.
  """
  args_parser = argparse.ArgumentParser(
    description='List artifact definitions.')

  args_parser.add_argument(
      'definitions', nargs='?', action='store', metavar='PATH',
      help=('path of the file or directory that contains the artifact '
            'definitions.'),
      default='./data')

  args_parser.add_argument(
      'os', choices=definitions.SUPPORTED_OS,
      help='show artifacts from operating system.')

  args_parser.add_argument(
      '--format',
      choices=['list', 'jsonl', 'csv'], default='list',
      help='the output format.')

  args_parser.add_argument('--show_docs', action='store_true',
      help='show docs value (only for list output format).')

  args_parser.add_argument('--split_paths', action='store_true',
      help='show separate entries for artifacts with more than one path.')

  options = args_parser.parse_args()

  if not options.definitions:
    print('Source value is missing.')
    print('')
    args_parser.print_help()
    print('')
    return False

  if not os.path.exists(options.definitions):
    print(f'No such file or directory: {options.definitions}')
    print('')
    return False

  artifact_lister = ArtifactLister(
      options.definitions, options.os, options.split_paths)
  if options.format == 'jsonl':
    artifact_lister.PrintJSONL()
  elif options.format == 'csv':
    artifact_lister.PrintCSV()
  else:
    artifact_lister.PrintArtifacts(options.show_docs)
  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
