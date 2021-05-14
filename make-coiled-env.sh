#!/bin/bash

# Install py-spy separately so it doesn't conflict with Cythonized distributed
cat > postbuild.sh <<EOF
#!/bin/bash

python3 -m pip install git+https://github.com/gjoseph92/scheduler-profilers.git@8d59e7f8b2ab59e22f0937557fefe388eac6ea61
EOF
coiled env create -n profiling --conda environment.yml --post-build postbuild.sh
rm postbuild.sh
