## ForensicArtifacts.com Artifact Repository

A free, community-sourced, machine-readable knowledge base of forensic artifacts
that the world can use both as an information source and within other tools.

The [ForensicArtifacts.com](http://forensicartifacts.com/) artifact repository
was forked from the [GRR project](https://github.com/google/grr) artifact
collection into a stand-alone repository that is not tool-specific. The GRR
developers will migrate to using this repository and make contributions here. In
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

## Artifact Definition Format

The artifact definition format is described in detail in the [Style Guide](https://github.com/ForensicArtifacts/artifacts/blob/master/docs/style_guide.adoc).

## Contact

[forensicartifacts@googlegroups.com](https://groups.google.com/forum/#!forum/forensicartifacts)
