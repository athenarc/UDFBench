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

MONETDBPORT=$MONETDBSSDPORT

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    MONETDBPORT=$MONETDBHDDPORT
elif [ $DISK = "mem" ]; then
    MONETDBPORT=$MONETDBMEMPORT
fi
shift


$MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance < "$MONETDBSCRIPTS"/monetdb_schema.sql
       