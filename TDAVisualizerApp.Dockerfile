# Dockerfile for TDA Visualizer App 1.0
# AUTHORS: Peter Mikulecky and Patrick Hudson
# DATE: 2/26/25

# Use a Python base image
FROM python:3.9-slim

# Augment base image with tkinter library
RUN apt-get update && apt-get install -y tk

# Set the working directory in the container
WORKDIR /TDA-project

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for host mounting
RUN mkdir /user-data

# Copy the source code into the container
COPY src/ ./src/

COPY entrypoint.sh .

# Ensure the entrypoint script is executable
RUN chmod +x ./entrypoint.sh

# Copy the tests folder (optional, if you want to run tests in Docker)
COPY tests/ ./tests/

# Copy other necessary files
COPY README.md .
COPY INSTALL.md .
COPY LICENSE.md .
COPY sample_wind.csv .
COPY sample_wind2.csv .

# Set the entrypoint to the wrapper script
ENTRYPOINT ["/TDA-project/entrypoint.sh"]
