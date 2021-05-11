#!/bin/bash

# Install py-spy separately so it doesn't conflict with Cythonized distributed
cat > postbuild.sh <<EOF
#!/bin/bash

python3 -m pip install git+https://github.com/gjoseph92/distributed-pyspy.git@e912bd5af0c84c699e3e38280b2789f1f0d6fc93
EOF
coiled env create -n profiling --conda environment.yml --post-build postbuild.sh
rm postbuild.sh
