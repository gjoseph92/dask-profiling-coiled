#!/bin/bash

# Install py-spy separately so it doesn't conflict with Cythonized distributed
cat > postbuild.sh <<EOF
#!/bin/bash

python3 -m pip install git+https://github.com/gjoseph92/scheduler-profilers.git@c3e02d33ab2bf7e99ff920563b38dfd92b2ce65b
EOF
coiled env create -n profiling --conda environment.yml --post-build postbuild.sh
rm postbuild.sh
