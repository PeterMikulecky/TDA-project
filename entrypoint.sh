#!/bin/bash

# Run your analysis app
python3 /TDA-project/src/main.py

# Copy all .png files to ../../user-data
cp /TDA-project/*.png /user-data/

# Start an interactive bash session
exec /bin/bash
