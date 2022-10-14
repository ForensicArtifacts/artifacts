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
supported_os: [Windows]
urls: ['https://artifacts-kb.readthedocs.io/en/latest/sources/windows/EventLog.html']
```

The artifact definition can have the following values:

Value | Description
--- | ---
aliases | Optional list of alternate names to identify the artifact definition. Also see: See section: [Name](#name).
doc | The description (or documentation). A human readable string that describes the artifact definition. See section: [Description](#description).
name | The name. An unique string that identifies the artifact definition. See section: [Name](#name).
provides | Optional list of *TODO*
sources | A list of source definitions. See section: [Sources](#sources).
supported_os | Optional list that indicates which operating systems the artifact definition applies to. See section: [Supported operating system](#supported-operating-system).
urls | Optional list of URLs with more contextual information. Ideally the artifact definition links to an article that discusses the artifact in more depth for example on [Digital Forensics Artifact Knowledge Base](https://github.com/ForensicArtifacts/artifacts-kb).

## Deprecated values

Value | Description
--- | ---
conditions | Optional list of conditions that describe when the artifact definition should apply. Note that conditions have been deprecated as of version 20220710.
labels | Optional list of predefined labels. Note that labels have been deprecated as of version 20220311.

## Name

The name of an artifact definition should be in CamelCase name without spaces.

Prefix platform specific artifact definitions with the name of the operating
system using "Linux", "MacOS" or "Windows".

If not platform specific:

* prefix with the application name, for example "ChromeHistory".
* prefix with the name of the subsystem, for example "WMIComputerSystemProduct".

Commonly used prefixes:

Prefix | Description
--- | ---
Darwin | Mac OS (or Darwin) operating system specific artifact definition.
Linux | Linux operating system specific artifact definition.
Shell | Shell user-interface specific artifact definition.
User | User specific artifact definition.
Unix | Unix operating system (or POSIX) specific artifact definition.
Windows | Windows operating system specific artifact definition.

Suffix artifact definitions with the type of artifact, for example are files use
"BrowserHistoryFile" instead of "BrowserHistory" to reduce ambiguity.

Suffix | Description
--- | ---
ConfigurationFile | Contents of one or more configuration files.
Directory | Contents of one or more directories.
File | Contents of one or more files.
LogFile | Contents of one or more log files.
PlistFile | Contents of one or more property list (plist) files.
SQLiteDatabaseFile | Contents of one or more SQLite database files.

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
supported_os | Optional list that indicates which operating systems the artifact definition applies to. See section: [Supported operating system](#supported-operating-system).

## Deprecated values

Value | Description
--- | ---
conditions | Optional list of conditions to when the artifact definition should apply. See section: Note that conditions have been deprecated as of version 20220710.

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
    names:
    - WindowsRunKeys
    - WindowsServices
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
separator | Optional path segment separator e.g. '\' for Windows systems. When not specified the default path segment separator is '/'.

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
separator | Optional path segment separator e.g. '\' for Windows systems. When not specified the default path segment separator is '/'.

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

## Supported operating system

Since operating system (OS) are a very common constraint, this has been provided
as a separate option "supported_os" to simplify syntax. For supported_os no
quotes are required. The currently supported operating systems are:

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

## Parameter expansion and globs

Artifact definitions can use different types of parameters that need to be
expanded at runtime, such as:

* POSIX users variables, for example %%users.homedir%%
* Windows evironment variables, for example %%environ_systemroot%%
* Windows users variables, for example %%users.temp%%

### POSIX users variables

Supported POSIX users variables are:

Variable | Description
--- | ---
%%users.homedir%% | A user's home directory, for example '/home/username', '/root' or '/Users/username'

#### Decomposition rules

Note that the following decomposition rules are approximations based on
common usage scenarios.

%%users.homedir%% can be decomposed into:

* '/Users/*' for Mac OS
* '/home/*' and '/root' for Linux

### Windows evironment variables

Supported Windows evironment variables are:

Variable | Description
--- | ---
%%environ_allusersappdata%% | The %AllUsersAppData% environment variable, which should fallback to the %ProgramData% environment variable if not available.
%%environ_allusersprofile%% | The %AllUsersProfile% environment variable.
%%environ_programdata%% | The %ProgramData% environment variable, which should fallback to the %AllUsersAppData% environment variable or '%AllUsersProfile%\\Application Data' if not available.
%%environ_programfiles%% | The %ProgramFiles% environment variable.
%%environ_programfilesx86%% | The %ProgramFiles(x86)% environment variable.
%%environ_systemdrive%% | The %SystemDrive% environment variable, for example 'C:'
%%environ_systemroot%% | The %SystemRoot% environment variable, for example 'C:\\Windows'
%%environ_windir%% | The %WinDir% environment variable, for example 'C:\\Windows'

### Windows users variables

Supported Windows users variables are:

Variable | Description
--- | ---
%%users.appdata%% | Windows version independent representation of a user specific %AppData% environment variable.
%%users.localappdata%% | Windows version independent representation of a user specific %LocalAppData% environment variable.
%%users.sid%% | A user's security identifier (SID)
%%users.temp%% | A user's temporary files directory, comparable to the %TEMP% or %TMP% environment variables, for example '/Users/username/temp'
%%users.username%% | A user's username, comparable to the %USERNAME% environment variable
%%users.userprofile%% | A user's (local) profile directory, for example '/Users/username'

#### Decomposition rules

**TODO: add information about system accounts**

Note that the following decomposition rules are approximations based on
common usage scenarios.

%%users.appdata%% can be decomposed into:

* '%%users.userprofile%%\\AppData\\Roaming' for Windows Vista and later
* '%%users.userprofile%%\\Application Data'

%%users.localappdata%% can be decomposed into:

* '%%users.userprofile%%\\AppData\\Local' for Windows Vista and later
* '%%users.userprofile%%\\Local Settings\\Application Data'

%%users.localappdata_low%% can be decomposed into:

* '%%users.userprofile%%\\AppData\\LocalLow' for Windows Vista and later

%%users.temp%% can be decomposed into:

* '%%users.localappdata%%\\Temp'

%%users.userprofile%% can be decomposed into:

* 'Documents and Settings\\*'
* 'Users\\*' for Windows Vista and later

## Additional style notes

### Artifact definition YAML files

Artifact definition YAML filenames should be of the form:

```
$FILENAME.yaml
```

Where $FILENAME is name of the file e.g. windows.yaml.

Each definition file should have a comment at the top of the file with a
one-line summary describing the type of artifact definitions contained in the
file e.g.

```yaml
# Windows specific artifacts.
```

### Lists

Generally use the short `[]` format for single-item lists that fit inside 80
characters to save on unnecessary line breaks:

```yaml
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
like supported_os.

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
supported_os attributes where it makes sense. e.g. rather than having
FirefoxHistoryWindows, FirefoxHistoryLinux, FirefoxHistoryDarwin, do:

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
supported_os: [Windows, Linux, Darwin]
```

