#!/bin/bash

# Install py-spy separately so it doesn't conflict with Cythonized distributed.
# Also add dask config.

# HACK: Coiled offers no easy way to add auxiliary data files---or a dask config---in software environments,
# so we generate a post-build shell script that has the contents of `dask.yaml` within itself, and writes
# those contents out when executed.
OUT_CONFIG_PATH="~/.config/dask/dask.yaml"
YAML_CONTENTS=$(<dask.yaml)
cat > postbuild.sh <<EOF
#!/bin/bash

python3 -m pip install git+https://github.com/gjoseph92/scheduler-profilers.git@8d59e7f8b2ab59e22f0937557fefe388eac6ea61

OUT_CONFIG_PATH=$OUT_CONFIG_PATH
# ^ NOTE: no quotes, so ~ expands (https://stackoverflow.com/a/32277036)
mkdir -p \$(dirname \$OUT_CONFIG_PATH)

cat > \$OUT_CONFIG_PATH <<INNER_EOF
$YAML_CONTENTS
INNER_EOF

echo "export DASK_CONFIG=\$OUT_CONFIG_PATH" >> ~/.bashrc

echo "Wrote dask config to \$OUT_CONFIG_PATH:"
cat \$OUT_CONFIG_PATH
EOF
coiled env create -n profiling --conda environment.yml --post-build postbuild.sh
rm postbuild.sh
