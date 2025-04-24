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

MONETDBPORT=$MONETDBSSDPORT

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then

    MONETDBPORT=$MONETDBHDDPORT
elif [ $DISK = "mem" ]; then
    MONETDBPORT=$MONETDBMEMPORT
fi
shift

DATABASE_STATUS=$("$MONETDBBINPATH/monetdb" status "$DATAB" 2>&1)

if echo "$DATABASE_STATUS" | grep -q "no such database"; then
    
    $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT create $DATAB
    $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT set embedc=true $DATAB
    $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT set embedpy3=true $DATAB
    $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT release $DATAB
    $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT start $DATAB
        
fi
