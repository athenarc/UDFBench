#!/bin/bash



# Check if the correct number of arguments is provided
if [ "$#" -lt 3 ]; then
    echo "Usage: $0  <database> <disk> <dataset>"
    exit 1
fi

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
shift

DATASETPATH="$1"
shift


DUCKDBPATH=$DUCKDBSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    DUCKDBPATH=$DUCKDBHDDPATH
elif [ $DISK = "mem" ]; then
    DUCKDBPATH=$DUCKDBMEMPATH
fi
shift




sed -i.bak "s|[^']*\.csv'|"$DATASETPATH/csvs/$DATAB"/&|g" "$DUCKDBSCRIPTS"/duckdb_load.sql;

"$DUCKDBCLI" "$DUCKDBPATH/$DATAB".db < "$DUCKDBSCRIPTS"/duckdb_load.sql;

mv "$DUCKDBSCRIPTS"/duckdb_load.sql.bak "$DUCKDBSCRIPTS"/duckdb_load.sql
