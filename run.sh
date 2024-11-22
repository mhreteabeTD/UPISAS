#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/UPISAS

# Run the experiment
python3 experiment-runner/experiment-runner/ UPISAS/experiment_runner_configs/Wildfire_UAV.py
