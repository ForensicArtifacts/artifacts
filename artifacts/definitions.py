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
"""Constants and definitions."""

# The type indictor constants.
TYPE_INDICATOR_ARTIFACT = 'ARTIFACT'
TYPE_INDICATOR_ENVIRONMENT = 'ENVIRONMENT'
TYPE_INDICATOR_FILE = 'FILE'
TYPE_INDICATOR_PATH = 'PATH'
TYPE_INDICATOR_REGISTRY_KEY = 'REGISTRY_KEY'
TYPE_INDICATOR_REGISTRY_VALUE = 'REGISTRY_VALUE'
TYPE_INDICATOR_WMI = 'WMI'

LABELS = {
    'Antivirus': 'Antivirus related artifacts, e.g. quarantine files.',
    'Authentication': 'Authentication artifacts.',
    'Browser': 'Web Browser artifacts.',
    'Configuration Files': 'Configuration files artifacts.',
    'Execution': 'Contain execution events.',
    'External Media': 'Contain external media data or events e.g. USB drives.',
    'KnowledgeBase': 'Artifacts used in knowledgebase generation.',
    'Logs': 'Contain log files.',
    'Memory': 'Artifacts retrieved from Memory.',
    'Network': 'Describe networking state.',
    'Processes': 'Describe running processes.',
    'Software': 'Installed software.',
    'System': 'Core system artifacts.',
    'Users': 'Information about users.',
    'Rekall': 'Artifacts using the Rekall memory forensics framework.',
    }

SUPPORTED_OS = frozenset(['Darwin', 'Linux', 'Windows'])
