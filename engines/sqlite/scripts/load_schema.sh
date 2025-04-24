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


SQLITEDBPATH=$SQLITEDBSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    SQLITEDBPATH=$SQLITEDBHDDPATH
elif [ $DISK = "mem" ]; then
    SQLITEDBPATH=$SQLITEDBMEMPATH
fi
shift


sed -i.bak "s|[^']*\.csv'|"$DATASETPATH/csvs/$DATAB"/&|g" "$SQLITESCRIPTS"/sqlite_load.sql;

"$SQLITEEXEC" "$SQLITEDBPATH/$DATAB".db  < "$SQLITESCRIPTS"/sqlite_load.sql;

mv "$SQLITESCRIPTS"/sqlite_load.sql.bak "$SQLITESCRIPTS"/sqlite_load.sql
