#!/bin/bash
# Script to update the version information.

EXIT_FAILURE=1;
EXIT_SUCCESS=0;

VERSION=`date -u +"%Y%m%d"`
DPKG_DATE=`date -R`

# Update the Python module version.
sed "s/__version__ = '[0-9]*'/__version__ = '${VERSION}'/" -i artifacts/__init__.py

# Update the version in the dpkg configuration files.
cat > config/dpkg/changelog << EOT
artifacts (${VERSION}-1) unstable; urgency=low

  * Auto-generated

 -- Forensic artifacts <forensicartifacts@googlegroups.com>  ${DPKG_DATE}
EOT

# Regenerate the statistics documentation.
cat > docs/sources/background/Stats.md << EOT
## Statistics

The artifact definitions can be found in the [data directory](https://github.com/ForensicArtifacts/artifacts/tree/main/data)
and the format is described in detail in the [Style Guide](https://github.com/ForensicArtifacts/artifacts/blob/main/docs/Artifacts%20definition%20format%20and%20style%20guide.asciidoc).
EOT

PYTHONPATH=. ./tools/stats.py >> docs/sources/background/Stats.md

# Regenerate the API documentation.
tox -edocs

exit ${EXIT_SUCCESS};
