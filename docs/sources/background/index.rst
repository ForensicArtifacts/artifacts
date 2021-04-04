##########
Background
##########

The first version of the artifact definitions originated from the
`GRR project <https://github.com/google/grr>`__, where it is used to describe
and quickly collect data of interest, for example specific files or Windows
Registry keys. The goal of the format is to provide a tool independent way to
describe the majority of forensic artifacts in a language that is readable by
humans and machines.

The format is designed to be simple and straight forward, so that a digital
forensic analysist is able to quickly write artifact definitions during an
investigation without having to rely on complex standards or tooling.

The format is intended to describe forensically-relevant data on a machine,
while being tool agnostic. In particular we intentionally avoided adding
IOC-like logic, or describing how the data should be collected since this
various between tools.

For some background on the artifacts system and how we expect it to be used see
`this Blackhat presentation <https://www.blackhat.com/us-14/archives.html#grr-find-all-the-badness-collect-all-the-things>`__
and `YouTube video <https://www.youtube.com/watch?v=ren6QSvwFvg>`__ from the GRR team.

.. toctree::
   :maxdepth: 2

   Terminology <Terminology>
   Statistics <Stats>
