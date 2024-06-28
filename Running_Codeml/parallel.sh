#!/bin/bash

# Define the main directory containing subdirectories
MAIN_DIR="/Users/kagarwal/Desktop/9560/contracted_input_paml"

# Export PATH or any other environment variables if codeml is not globally accessible
# export PATH=$PATH:/path/to/codeml

# Use GNU Parallel to run codeml in each subdirectory
# -j 3 means run 3 jobs in parallel
# --workdir ... sets the working directory for each job to the directory found

find $MAIN_DIR -mindepth 1 -maxdepth 1 -type d | parallel -j 5 --workdir '{}' codeml /Users/kagarwal/Desktop/9560/codeml.ctl
