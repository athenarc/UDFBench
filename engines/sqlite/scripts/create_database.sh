#parameters: s|m|l - duckdb|monetdb|postgres|sqlite3 -ssd|hdd|mem

#!/bin/bash

export CURRENT=$PWD

# Check if the correct number of arguments is provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <database> <disk> "
    exit 1
fi


#  database file
DATABASE="$1"
shift


DATAB="tiny"
    case $DATABASE in
        t)
            DATAB="tiny"
            ;;
        s)
            DATAB="small"
            ;;
        m)
            DATAB="medium"
            ;;
        l)
            DATAB="large"
            ;;
        *)
            echo "Invalid input"
            ;;
    esac

DISK="$1"

SQLITEDBPATH=$SQLITEDBSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    SQLITEDBPATH=$SQLITEDBHDDPATH
elif [ $DISK = "mem" ]; then
    SQLITEDBPATH=$SQLITEDBMEMPATH
fi
shift

touch "$SQLITEDBPATH/$DATAB".db
