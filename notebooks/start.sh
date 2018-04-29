#!/bin/bash
jupyter notebook --notebook-dir=/notebooks --no-browser --allow-root \
    --no-mathjax --config=/jupyter_notebook_config.py --ip=* --log-level=DEBUG