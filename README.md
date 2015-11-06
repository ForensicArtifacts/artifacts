## ForensicArtifacts.com Artifact Repository [![Build Status](https://travis-ci.org/ForensicArtifacts/artifacts.svg?branch=master)](https://travis-ci.org/ForensicArtifacts/artifacts)

A free, community-sourced, machine-readable knowledge base of forensic artifacts
that the world can use both as an information source and within other tools.

If you'd like to use the artifacts in your own tools, **all you need to be able to do is read YAML**. That's it.  No other dependencies. The python code in this project is just used to validate all the artifacts to make sure they follow the spec.

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

We love contributions! If you're contributing artifacts, please follow the
[Style Guide](https://github.com/ForensicArtifacts/artifacts/blob/master/docs/style_guide.adoc)
and make sure the tests pass:

```
$ python run_tests.py
```

If you're contributing python code, check with us on the mailing list first,
especially if it's something big.

We use the github [fork and pull review
process](link:https://help.github.com/articles/using-pull-requests) to review
all contributions. First, fork the [Artifact
repository](https://github.com/ForensicArtifacts/artifacts) by following [the
github instructions](https://help.github.com/articles/fork-a-repo).

Now that you have a github.com/your-username/artifacts repository, make your
changes. When you're ready for review, [sync your branch with
upstream](https://help.github.com/articles/syncing-a-fork):

```
$ git fetch upstream
$ git merge upstream/master

# Fix any conflicts and commit your changes with a description
$ git commit -a
$ git push
```

and use the GitHub Web UI to [create and send the pull
request](https://help.github.com/articles/using-pull-requests).  We'll review
and merge the change.

## Artifact Definitions

The artifact definitions are in the [definitions directory](https://github.com/ForensicArtifacts/artifacts/tree/master/definitions) and the format is described in detail in the [Style Guide](https://github.com/ForensicArtifacts/artifacts/blob/master/docs/Artifacts%20definition%20format%20and%20style%20guide.asciidoc).

## Contributing

Please send us your contribution! See [the developers guide](https://github.com/ForensicArtifacts/artifacts/wiki/Developers-guide) for instructions.

## External links
* [ForensicsArtifacts.com ... the definitive database](http://forensicartifacts.com/)
* [GRR Artifacts](https://www.blackhat.com/docs/us-14/materials/us-14-Castle-GRR-Find-All-The-Badness-Collect-All-The-Things-WP.pdf), by Greg Castle, Blackhat 2014

## Contact

[forensicartifacts@googlegroups.com](https://groups.google.com/forum/#!forum/forensicartifacts)
