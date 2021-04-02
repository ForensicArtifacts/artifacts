# History

The first version of the artifact definitions originated from the
[GRR project](https://github.com/google/grr), where it is used to describe and
quickly collect data of interest, e.g. specific files or Windows Registry keys.
The goal of the format is to provide a way to describe the majority of forensic
artifacts in a language that is readable by humans and machines.

The format is designed to be simple and straight forward, so that a digital
forensic analysist is able to quickly write artifact definitions during an
investigation without having to rely on complex standards or tooling.

The format is intended to describe forensically-relevant data on a machine,
while being tool agnostic. In particular we intentionally avoided adding
IOC-like logic, or describing how the data should be collected since this
various between tools.
