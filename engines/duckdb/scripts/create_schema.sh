#!/bin/bash


if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <database> <disk> "
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

DUCKDBPATH=$DUCKDBSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    DUCKDBPATH=$DUCKDBHDDPATH
elif [ $DISK = "mem" ]; then
    DUCKDBPATH=$DUCKDBMEMPATH
fi
shift

"$DUCKDBCLI" "$DUCKDBPATH/$DATAB".db < "$DUCKDBSCRIPTS"/duckdb_schema.sql
