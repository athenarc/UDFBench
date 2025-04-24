#!/bin/bash


#Set up MonetDB from source and configure with Python


if [ "$#" -lt 1 ]; then
    echo "Usage: $0  <pythonexec> "
    exit 1
fi

PYTHONEXEC="$1"
shift

# create a `.monetdb` file at your home dir:
touch ~/.monetdb
echo user=monetdb > ~/.monetdb
echo password=monetdb >> ~/.monetdb

# Install Python dependencies for Python 3
# "$PYTHONEXEC" -m pip install pandas numpy nltk --upgrade


# Set the current directory to a variable

export CURRENT=$PWD

mkdir -p  $PWD'/downloads/monetdb'
cd $PWD'/downloads/monetdb'

#Clone the MonetDB repository
git clone https://github.com/MonetDB/MonetDB.git



cd MonetDB

# # Create a 'build' directory
# rm -r build
mkdir build
cd build

# Create a directory 'monetdb' inside the directory stored in $MONETDBDIRPATH
mkdir -p "$MONETDBDIRPATH"

# Configure MonetDB using CMake
cmake -DCMAKE_INSTALL_PREFIX=$MONETDBDIRPATH   ../

#Build and install MonetDB
cmake --build .
cmake --build . --target install

# Return to the original directory
cd $MONETDBDIRPATH

# # Create and start a MonetDB database instance
"$MONETDBDIRPATH/bin/monetdbd" create "$MONETDBINSTANCE"
"$MONETDBDIRPATH/bin/monetdbd" set port="$MONETDBSSDPORT" "$MONETDBINSTANCE"
"$MONETDBDIRPATH/bin/monetdbd" start "$MONETDBINSTANCE"


#Create and start MonetDB databases named tiny, small, medium,large:
# for database in tiny small medium large; do
#     $MONETDBDIRPATH/bin/monetdb -p $MONETDBSSDPORT create $database
#     $MONETDBDIRPATH/bin/monetdb -p $MONETDBSSDPORT set embedc=true $database
#     $MONETDBDIRPATH/bin/monetdb -p $MONETDBSSDPORT set embedpy3=true $database
#     $MONETDBDIRPATH/bin/monetdb -p $MONETDBSSDPORT release $database
#     $MONETDBDIRPATH/bin/monetdb -p $MONETDBSSDPORT start $database
# done

cd $CURRENT