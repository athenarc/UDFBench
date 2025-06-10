#!/bin/bash

#Set up Spark from source and configure with Python

if [ "$#" -lt 1 ]; then
    echo "Usage: $0  <pythonexec> "
    exit 1
fi

PYTHONEXEC="$1"
shift
export CURRENT=$PWD

mkdir -p  $PWD'/downloads/pyspark'
cd $PWD'/downloads/pyspark'

wget https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5.tgz

tar -xvzf spark-3.5.5.tgz


# echo "export SPARK_HOME=$PWD/spark-3.5.5" >> ~/.bashrc
# echo "export PATH=\$SPARK_HOME/bin:\$SPARK_HOME/sbin:\$PATH" >> ~/.bashrc

# source ~/.bashrc
cd $CURRENT
