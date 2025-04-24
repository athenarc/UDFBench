#!/bin/bash


#Set up DuckDB install Python dependencies and download the DuckDB CLI
if [ "$#" -lt 1 ]; then
    echo "Usage: $0  <pythonexec> "
    exit 1
fi

PYTHONEXEC="$1"
shift
# Install Python dependencies for Python 3
# $PYTHONEXEC -m pip install apsw duckdb pyarrow pandas numpy nltk --upgrade

# Set environment variables
export CURRENT=$PWD

# Create a directory for DuckDB CLI and navigate to it
mkdir -p $DUCKDBPATH
mkdir -p $DUCKDBPATH/cli
cd $DUCKDBPATH/cli

# Download DuckDB CLI
wget https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip

# Unzip the downloaded file
unzip duckdb_cli-linux-amd64.zip

# Remove the downloaded zip file
rm duckdb_cli-linux-amd64.zip


cd $CURRENT