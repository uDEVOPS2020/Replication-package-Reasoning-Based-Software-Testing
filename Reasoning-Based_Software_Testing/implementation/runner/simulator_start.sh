#!/bin/bash
export PYLOT_HOME=/home/erdos/workspace/pylot/
export PYTHONPATH=/home/erdos/workspace/pylot/dependencies/:/home/erdos/workspace/pylot/dependencies/CARLA_0.9.10.1/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg:/home/erdos/workspace/pylot/dependencies/CARLA_0.9.10.1/PythonAPI/carla/:/home/erdos/workspace/pylot/dependencies/CARLA_0.9.10.1/PythonAPI/carla/agents/:/home/erdos/workspace/pylot/dependencies/CARLA_0.9.10.1/PythonAPI/:/home/erdos/workspace/scenario_runner:$PYLOT_HOME/dependencies/lanenet/

python3 pylot.py --flagfile=configs/e2e.conf
