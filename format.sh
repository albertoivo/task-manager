#!/bin/bash

# This script formats the code in the 'app' directory using various tools.

# Ensure the script is run from the root directory of the project
if [ ! -d "app" ]; then
  echo "The 'app' directory does not exist. Please run this script from the root of the project."
  exit 1
fi

# Format the code using black, isort, and autoflake
echo "Formatting code in the 'app' directory..."
black app/
isort app/
autoflake --remove-all-unused-imports --remove-unused-variables --remove-duplicate-keys --expand-star-imports --ignore-init-module-imports --recursive --in-place app/