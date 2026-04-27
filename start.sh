#!/bin/bash

# Activate the virtual environment
source /home/mohamed/ros2_ws/env/bin/activate

# Add the venv packages to the Python Path
export PYTHONPATH=/home/mohamed/ros2_ws/env/lib/python3.12/site-packages:$PYTHONPATH

source install/setup.bash

echo "✅ Environment activated and PYTHONPATH updated!"
