#!/bin/bash
set -e

# Install py-spy separately so it doesn't conflict with Cythonized distributed
cat > postbuild.sh <<EOF
#!/bin/bash

python3 -m pip install git+https://github.com/gjoseph92/scheduler-profilers.git@2691c0fc79e4f4fc9e90c7cfcbdf153f45107d36
EOF
coiled env create -n profiling --conda environment.yml --post-build postbuild.sh
rm postbuild.sh

python make-coiled-notebook.py
