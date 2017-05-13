## ForensicArtifacts.com Artifact Repository [![Build Status](https://travis-ci.org/ForensicArtifacts/artifacts.svg?branch=master)](https://travis-ci.org/ForensicArtifacts/artifacts)

A free, community-sourced, machine-readable knowledge base of forensic artifacts
that the world can use both as an information source and within other tools.

If you'd like to use the artifacts in your own tools, **all you need to be able to do is read YAML**. That's it.  No other dependencies. The python code in this project is just used to validate all the artifacts to make sure they follow the spec.

## Artifact Definitions

The artifact definitions are in the [definitions directory](https://github.com/ForensicArtifacts/artifacts/tree/master/definitions) and the format is described in detail in the [Style Guide](https://github.com/ForensicArtifacts/artifacts/blob/master/docs/Artifacts%20definition%20format%20and%20style%20guide.asciidoc).

As of 2015-11-20 the repository contains:

| **File paths covered** | **487** |
| :------------------ | ------: |
| **Registry keys covered** | **289** |
| **Total artifacts** | **345** |

**Artifacts by type**

|  ARTIFACT | COMMAND | DIRECTORY | FILE | PATH | REGISTRY_KEY | REGISTRY_VALUE | WMI | 
|  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: | 
|  14 | 6 | 11 | 191 | 4 | 38 | 65 | 16 | 

**Artifacts by OS**

|  Darwin | Linux | Windows | 
|  :---: |  :---: |  :---: | 
|  106 | 75 | 177 | 

**Artifacts by label**

|  Antivirus | Authentication | Browser | Cloud | Cloud Storage | Configuration Files | External Media | ExternalAccount | IM | Logs | Mail | Network | Software | System | Users | iOS | 
|  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: |  :---: | 
|  6 | 12 | 18 | 2 | 3 | 34 | 2 | 3 | 4 | 27 | 12 | 7 | 35 | 62 | 59 | 5 | 

## Background/History

The [ForensicArtifacts.com](http://forensicartifacts.com/) artifact repository
was forked from the [GRR project](https://github.com/google/grr) artifact
collection into a stand-alone repository that is not tool-specific. The GRR
developers have migrated to using this repository and make contributions here. In
addition the ForensicArtifact team will begin backfilling artifacts in the new
format from the [ForensicArtifacts.com](http://forensicartifacts.com/) website.

For some background on the artifacts system and how we expect it to be used see
[this blackhat presentation](https://www.blackhat.com/us-14/archives.html#grr-find-all-the-badness-collect-all-the-things)
and [youtube video](http://www.youtube.com/watch?v=DudGrSv26NY) from the GRR
team.

## Contributing

Please send us your contribution! See [the developers guide](https://github.com/ForensicArtifacts/artifacts/wiki/Developers-guide) for instructions.

## External links
* [ForensicsArtifacts.com ... the definitive database](http://forensicartifacts.com/)
* [GRR Artifacts](https://www.blackhat.com/docs/us-14/materials/us-14-Castle-GRR-Find-All-The-Badness-Collect-All-The-Things-WP.pdf), by Greg Castle, Blackhat 2014

## Contact

[forensicartifacts@googlegroups.com](https://groups.google.com/forum/#!forum/forensicartifacts)
