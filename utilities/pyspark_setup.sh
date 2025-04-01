#!/bin/bash

export CURRENT=$PWD

mkdir -p  $PWD'/downloads/pyspark'
cd $PWD'/downloads/pyspark'

wget https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5.tgz

tar -xvzf spark-3.5.5.tgz

echo "export SPARK_HOME=$PWD'/spark-3.5.5" >> ~/.bashrc
echo "export PATH=\$SPARK_HOME/bin:\$SPARK_HOME/sbin:\$PATH" >> ~/.bashrc

cd $CURRENT
