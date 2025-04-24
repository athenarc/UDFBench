#!/bin/bash

#Set up PostgreSQL from source and configure with Python

if [ "$#" -lt 1 ]; then
    echo "Usage: $0  <pythonexec> "
    exit 1
fi

PYTHONEXEC="$1"
shift
# cd $PWD'/downloads'
mkdir -p  $PWD'/downloads/postgres'
cd $PWD'/downloads/postgres'
#Clone the PostgreSQL repository
git clone https://github.com/postgres/postgres.git

export POSTPATH=$POSTGRESPATH
# Create a local PostgreSQL folder on folder databases
mkdir "$POSTPATH"

cd postgres
git checkout REL_17_STABLE
git branch

# Ensure that Python and required packages are installed before configuring PostgreSQL (PL/Python supports only Python 3)
# Install Python dependencies for the default Python 
# "$PYTHONEXEC" -m pip install pandas numpy nltk --upgrade  --user

# Configure PostgreSQL with default Python 3
./configure --prefix=$POSTPATH --with-python PYTHON="$PYTHONEXEC"

# (Optional)  Install Python dependencies for Python 3.10
# python3.10 -m pip install pandas numpy nltk --upgrade

# (Optional)  Configure PostgreSQL with Python 3.10
# ./configure --prefix=$POSTPATH --with-python PYTHON=/usr/bin/python3.10

#Build and install PostgreSQL
make
make install

#Create the data directory
mkdir $POSTPATH/data

#Initialize a new database cluster
$POSTPATH/bin/initdb -D $POSTPATH/data

#Change the port (from default 5432)
cd $POSTPATH/data
sed -i "/#port = 5432/c\port = $PSQLSSDPORT" postgresql.conf # Uncomment the line #port = 5432 and change it to your port number ($PSQLSSDPORT)

#Start the server and create the database
$POSTPATH/bin/pg_ctl -D $POSTPATH/data -l logfile start

# for database in tiny small medium large; do
#     $POSTPATH/bin/createdb -U $PSQLUSER -p $PSQLSSDPORT $database 
# done

#(Optional) Connect to the database using psql
#$POSTPATH/bin/psql -U $PSQLUSER -p $PSQLSSDPORT $DATAB 

# (Optional) Stop the server
#$POSTPATH/bin/pg_ctl -D $POSTPATH/data -w stop
