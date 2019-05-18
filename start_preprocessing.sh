#!/bin/bash

SECONDS=0

echo "Starting file checking"
python3.6 src/file_checker.py
echo "All files checked, logs @logs/file_checker.log"

echo "Starting preprocessing"
python3.6 src/data_preprocessing.py
echo "All files processed, logs @logs/data_preprocessing.log"

echo "Time elapsed: $SECONDS s"