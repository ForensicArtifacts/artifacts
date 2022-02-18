# -*- coding: utf-8 -*-
"""Constants and definitions."""

from __future__ import unicode_literals

TYPE_INDICATOR_ARTIFACT_GROUP = 'ARTIFACT_GROUP'
TYPE_INDICATOR_COMMAND = 'COMMAND'
TYPE_INDICATOR_DIRECTORY = 'DIRECTORY'
TYPE_INDICATOR_FILE = 'FILE'
TYPE_INDICATOR_PATH = 'PATH'
TYPE_INDICATOR_WINDOWS_REGISTRY_KEY = 'REGISTRY_KEY'
TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE = 'REGISTRY_VALUE'
TYPE_INDICATOR_WMI_QUERY = 'WMI'

LABELS = {
    'Antivirus': '<Deprecated>', # TODO: to be deleted
    'Applications': (
        'Configuration files and logs of installed applications '
        'e.g. Nginx log files.'),
    'Authentication': 'Authentication artifacts.',
    'Browser': 'Web Browser artifacts.',
    'Cloud': 'Cloud applications artifacts.',
    'Cloud Storage': 'Cloud storage artifacts.',
    'Configuration Files': 'Configuration files artifacts.',
    'Containerd': 'Containerd artifacts',
    'Docker': 'Docker artifacts.',
    'Execution': 'Contain execution events.',
    'ExternalAccount': '<Deprecated>', # TODO: to be deleted
    'External Account': (
        'Information about any user accounts e.g. username, '
        'account ID, etc.'),
    'External Media': 'Contain external media data or events e.g. USB drives.',
    'File System': 'Artifacts related to the file system e.g. MFT.',
    'Hadoop': 'Hadoop artifacts.',
    'IM': 'Instant Messaging / Chat applications artifacts.',
    'Interactive': 'Artifacts created by interactive (e.g. RDP) user activity.',
    'iOS': 'Artifacts related to iOS devices connected to the system.',
    'History Files': 'History files artifacts e.g. .bash_history.',
    'KnowledgeBase': '<Deprecated>', # TODO: to be deleted
    'Knowledge Base': 'Artifacts used in knowledge base generation.',
    'Kubernetes': 'Kubernetes artifacts',
    'Logs': 'Contain log files.',
    'Mail': 'Mail client applications artifacts.',
    'Memory': 'Artifacts retrieved from memory.',
    'Network': 'Describe networking state.',
    'Persistence' : 'Persistence mechanisms e.g. the Startup folder.',
    'Plist': 'Artifact that is a plist.',
    'Processes': 'Describe running processes.',
    'Rekall': 'Artifacts using the Rekall memory forensics framework.',
    'Registry': 'Files related to the Windows Registry.',
    'Security Agents': 'Endpoint detection and response related artifacts, '
        'e.g. antivirus quarantine files.',
    'Software': 'Information about installed software.',
    'SQLiteDB': 'Artifact that is a SQLite database.',
    'System': 'Core system artifacts.',
    'Users': 'Information about users.'
}

SUPPORTED_OS_DARWIN = 'Darwin'
SUPPORTED_OS_LINUX = 'Linux'
SUPPORTED_OS_WINDOWS = 'Windows'

SUPPORTED_OS = frozenset([
    SUPPORTED_OS_DARWIN,
    SUPPORTED_OS_LINUX,
    SUPPORTED_OS_WINDOWS])

TOP_LEVEL_KEYS = frozenset([
    'conditions',
    'doc',
    'labels',
    'name',
    'provides',
    'sources',
    'supported_os',
    'urls'])
