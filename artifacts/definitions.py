# -*- coding: utf-8 -*-
"""Constants and definitions."""

TYPE_INDICATOR_ARTIFACT_GROUP = 'ARTIFACT_GROUP'
TYPE_INDICATOR_COMMAND = 'COMMAND'
TYPE_INDICATOR_DIRECTORY = 'DIRECTORY'  # deprecated use PATH instead.
TYPE_INDICATOR_FILE = 'FILE'
TYPE_INDICATOR_PATH = 'PATH'
TYPE_INDICATOR_WINDOWS_REGISTRY_KEY = 'REGISTRY_KEY'
TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE = 'REGISTRY_VALUE'
TYPE_INDICATOR_WMI_QUERY = 'WMI'

SUPPORTED_OS_DARWIN = 'Darwin'
SUPPORTED_OS_ESXI = 'ESXi'
SUPPORTED_OS_LINUX = 'Linux'
SUPPORTED_OS_WINDOWS = 'Windows'

SUPPORTED_OS = frozenset([
    SUPPORTED_OS_DARWIN,
    SUPPORTED_OS_ESXI,
    SUPPORTED_OS_LINUX,
    SUPPORTED_OS_WINDOWS])

TOP_LEVEL_KEYS = frozenset([
    'aliases',
    # conditions have been deprecated as of version 20220710.
    'conditions',
    'doc',
    # labels have been deprecated as of version 20220311.
    'labels',
    'name',
    'provides',
    'sources',
    'supported_os',
    'urls'])
