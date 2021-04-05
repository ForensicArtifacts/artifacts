# Artifact definition format and style guide

The best way to show what an artifact definition is, is by example. The
following example is the artifact definition for the Windows EVTX System Event
Logs.

```yaml
name: WindowsSystemEventLogEvtx
doc: Windows System Event log for Vista or later systems.
sources:
- type: FILE
  attributes: {paths: ['%%environ_systemroot%%\System32\winevt\Logs\System.evtx']}
conditions: [os_major_version >= 6]
labels: [Logs]
supported_os: [Windows]
urls: ['https://artifacts-kb.readthedocs.io/en/latest/sources/windows/EventLog.html']
```

The artifact definition can have the following values:

Value | Description
--- | ---
name | The name. An unique string that identifies the artifact definition. See section: [Name](#name).
doc | The description (or documentation). A human readable string that describes the artifact definition. See section: [Description](#description).
sources | A list of source definitions. See section: [Sources](#sources).
conditions | Optional list of conditions that describe when the artifact definition should apply. See section: [Conditions](#conditions).
labels | Optional list of predefined labels. See section: [Labels](#labels).
provides | Optional list of *TODO*
supported_os | Optional list that indicates which operating systems the artifact definition applies to. See section: [Supported operating system](#supported-operating-system).
urls | Optional list of URLs with more contextual information. Ideally the artifact definition links to an article that discusses the artifact in more depth for example on [Digital Forensics Artifact Knowledge Base](https://github.com/ForensicArtifacts/artifacts-kb).

## Name

**Style note**: The name of an artifact defintion should be in CamelCase name
without spaces.

As of July 2016 we are migrating to the following naming convention:

* Prefix platform specific artifact definitions with the name of the operating system using "Linux", "MacOS" or "Windows"
* If not platform specific:
** prefix with the application name, for example "ChromeHistory".
** prefix with the name of the subsystem, for example "WMIComputerSystemProduct".

**Style note**: If the sole source of the artifact definition for example are
files use "BrowserHistoryFiles" instead of "BrowserHistory" to reduce ambiguity.

## Description

**Style note**: Typically one line description of the artifact, mentioning
important caveats. If more than one line is necessary, use the multi-line YAML
Literal Style as indicated by the `|` character.

```yaml
doc: |
  The Windows run keys.

  Note users.sid will currently only expand to SIDs with profiles on the system,
  not all SIDs.
```

**Style note**: the short description (first line) and the longer portion are
separated by an empty line.

**Style note**: explicit newlines (\n) should not be used.

## Sources

Every source definition starts with a `type` followed by arguments for example:

```yaml
sources:
- type: COMMAND
  attributes:
    args: [-qa]
    cmd: /bin/rpm
```

```yaml
sources:
- type: FILE
  attributes:
    paths:
    - /root/.bashrc
    - /root/.cshrc
    - /root/.ksh
    - /root/.logout
    - /root/.profile
    - /root/.tcsh
    - /root/.zlogin
    - /root/.zlogout
    - /root/.zprofile
    - /root/.zprofile
```

**Style note**: where sources take a single argument with a single value, the
one-line {} form should be used to save on line breaks as below:

```yaml
- type: FILE
  attributes: {paths: ['%%environ_systemroot%%\System32\winevt\Logs\System.evtx']}
```

Value | Description
--- | ---
attributes | A dictionary of keyword attributes specific to the type of source definition.
type | The source type.
conditions | Optional list of conditions to when the artifact definition should apply. See section: [Conditions](#conditions).
supported_os | Optional list that indicates which operating systems the artifact definition applies to. See section: [Supported operating system](#supported-operating-system).

### Source types

Currently the following different source types are defined:

Value | Description
--- | ---
ARTIFACT_GROUP | A source that consists of a group of other artifacts.
COMMAND | A source that consists of the output of a command.
FILE | A source that consists of the contents of files.
PATH | A source that consists of the contents of paths.
REGISTRY_KEY | A source that consists of the contents of Windows Registry keys.
REGISTRY_VALUE | A source that consists of the contents of Windows Registry values.
WMI | A source that consists of the output of Windows Management Instrumentation (WMI) queries.

The sources types are defined in
[definitions.py](https://github.com/ForensicArtifacts/artifacts/blob/main/artifacts/definitions.py).
as TYPE_INDICATOR constants.

### Artifact group source

The artifact group source is a source that consists of a group of other artifacts e.g.

```yaml
- type: ARTIFACT_GROUP
  attributes:
    names: [WindowsRunKeys, WindowsServices]
```

Where `attributes` can contain the following values:

Value | Description
--- | ---
names | A list of artifact definition names that make up this "composite" artifact. This can also be used to group multiple artifact definitions into one for convenience.

### Command source

The command source is a source that consists of the output of a command e.g.

```yaml
- type: COMMAND
  attributes:
    args: [-qa]
    cmd: /bin/rpm
```

Where `attributes` can contain the following values:

Value | Description
--- | ---
args | A list arguments to pass to the command.
cmd | The path of the command.

### File source

The file source is a source that consists of the contents of files e.g.

```yaml
- type: FILE
  attributes:
    paths: ['%%environ_systemroot%%\System32\winevt\Logs\System.evtx']
```

Where `attributes` can contain the following values:

Value | Description
--- | ---
paths | A list of file paths that can potentially be collected. The paths can use parameter expansion e.g. `%%environ_systemroot%%`. See section: [Parameter expansion and globs](parameter-expansion-and-globs).
separator | Optional path segment seperator e.g. '\' for Windows systems. When not specified the default path segment separator is '/'.

### Path source

The path source is a source that consists of the contents of paths e.g.

```yaml
- type: PATH
  attributes:
    paths: ['\Program Files']
    separator: '\'
```

Where `attributes` can contain the following values:

Value | Description
--- | ---
paths | A list of file paths that can potentially be collected. The paths can use parameter expansion e.g. `%%environ_systemroot%%`. See section: [Parameter expansion and globs](parameter-expansion-and-globs).
separator | Optional path segment seperator e.g. '\' for Windows systems. When not specified the default path segment separator is '/'.

### Windows Registry key source

The Windows Registry key source is a source that consists of the contents of
Windows Registry keys e.g.

```yaml
sources:
- type: REGISTRY_KEY
  attributes:
    keys:
    - 'HKEY_USERS\%%users.sid%%\Software\Microsoft\Internet Explorer\TypedURLs\*'
```

Where `attributes` can contain the following values:

Value | Description
--- | ---
keys | A list of Windows Registry key paths that can potentially be collected. The paths can use parameter expansion e.g. `%%users.sid%%`. See section: [Parameter expansion and globs](parameter-expansion-and-globs).

### Windows Registry value source

The Windows Registry value source is a source that consists of the contents of
Windows Registry values e.g.

```yaml
- type: REGISTRY_VALUE
  attributes:
    key_value_pairs:
    - {key: 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\WindowsUpdate', value: 'CISCNF4654'}
```

Where `attributes` can contain the following values:

Value | Description
--- | ---
key_value_pairs | A list of Windows Registry key paths and value names that can potentially be collected. The key path can use parameter expansion e.g. `%%users.sid%%`. See section: [Parameter expansion and globs](parameter-expansion-and-globs).

### Windows Management Instrumentation (WMI) query source

The  Windows Management Instrumentation (WMI) query source is a source that
consists of the output of Windows Management Instrumentation (WMI) queries e.g.

```yaml
- type: WMI
  attributes:
    query: SELECT * FROM Win32_UserAccount WHERE name='%%users.username%%'
```

Where `attributes` can contain the following values:

Value | Description
--- | ---
base_object | Optional WMI base object e.g. `winmgmts:\root\SecurityCenter2`
query | The Windows Management Instrumentation (WMI) query. The query can use parameter expansion e.g. `%%users.username%%`. See section: [Parameter expansion and globs](parameter-expansion-and-globs).

## Conditions

*TODO: work is in progress to move this out of GRR into something more portable.*

Artifact conditions are currently implemented using the
link:https://github.com/google/objectfilter[objectfilter] system that allows
you to apply complex conditions to the attributes of an object. Artifacts can
apply conditions to any of the Knowledge Base object attributes as defined in
the GRR link:https://github.com/google/grr/blob/master/proto/knowledge_base.proto[knowledge_base.proto].

**Style note**: single quotes should be used for strings when writing conditions.

```yaml
conditions: [os_major_version >= 6 and time_zone == 'America/Los_Angeles']
```

## Supported operating system

Since operating system (OS) conditions are a very common constraint, this has
been provided as a separate option "supported_os" to simplify syntax. For
supported_os no quotes are required. The currently supported operating systems
are:

* Darwin (also used for Mac OS X)
* Linux
* Windows

```yaml
supported_os: [Darwin, Linux, Windows]
```

This can be translated to objectfilter as:

```yaml
["os =='Darwin'" OR "os=='Linux'" OR "os == 'Windows'"]
```

## Labels

Currently the following different labels are defined:

Value | Description
--- | ---
Antivirus | Antivirus related artifacts, e.g. quarantine files.
Authentication | Authentication artifacts.
Browser | Web Browser artifacts.
Cloud Storage | Cloud Storage artifacts.
Configuration Files | Configuration files artifacts.
Execution | Contain execution events.
External Media | Contain external media data or events e.g. USB drives.
KnowledgeBase | Artifacts used in knowledge base generation.
Logs | Contain log files.
Memory | Artifacts retrieved from memory.
Network | Describe networking state.
Processes | Describe running processes.
Software | Installed software.
System | Core system artifacts.
Users | Information about users.

The labes are defined in
link:https://github.com/ForensicArtifacts/artifacts/blob/main/artifacts/definitions.py[definitions.py].

## Parameter expansion and globs

**TODO: add text**

## Additional style notes

### Artifact definition YAML files

Artifact definition YAML filenames should be of the form:

```
$FILENAME.yaml
```

Where $FILENAME is name of the file e.g. windows.yaml.

Each defintion file should have a comment at the top of the file with a
one-line summary describing the type of artifact definitions contained in the
file e.g.

```yaml
# Windows specific artifacts.
```

### Lists

Generally use the short `[]` format for single-item lists that fit inside 80
characters to save on unnecessary line breaks:

```yaml
labels: [Logs]
supported_os: [Windows]
urls: ['https://artifacts-kb.readthedocs.io/en/latest/sources/windows/EventLog.html']
```

and the bulleted list form for multi-item lists or long lines:

```yaml
paths:
- 'HKEY_USERS\%%users.sid%%\Software\Microsoft\Windows\CurrentVersion\Run\*'
- 'HKEY_USERS\%%users.sid%%\Software\Microsoft\Windows\CurrentVersion\RunOnce\*'
- 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run\*'
- 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce\*'
- 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnceEx\*'
```

### Quotes

Quotes should not be used for doc strings, artifact names, and simple lists
like labels and supported_os.

Paths and URLs should use single quotes to avoid the need for manual escaping.

```yaml
paths: ['%%environ_temp%%\*.exe']
urls: ['https://artifacts-kb.readthedocs.io/en/latest/sources/windows/EventLog.html']
```

Double quotes should be used where escaping causes problems, such as
regular expressions:

```yaml
content_regex_list: ["^%%users.username%%:[^:]*\n"]
```

### Minimize the number of definitions by using multiple sources

To minimize the number of artifacts in the list, combine them using the
supported_os and conditions attributes where it makes sense. e.g. rather than
having FirefoxHistoryWindows, FirefoxHistoryLinux, FirefoxHistoryDarwin, do:

```yaml
name: FirefoxHistory
doc: Firefox places.sqlite files.
sources:
- type: FILE
  attributes:
    paths:
    - %%users.localappdata%%\Mozilla\Firefox\Profiles\*\places.sqlite
    - %%users.appdata%%\Mozilla\Firefox\Profiles\*\places.sqlite
  supported_os: [Windows]
- type: FILE
  attributes:
    paths: [%%users.homedir%%/Library/Application Support/Firefox/Profiles/*/places.sqlite]
  supported_os: [Darwin]
- type: FILE
  attributes:
    paths: ['%%users.homedir%%/.mozilla/firefox/*/places.sqlite']
  supported_os: [Linux]
labels: [Browser]
supported_os: [Windows, Linux, Darwin]
```

