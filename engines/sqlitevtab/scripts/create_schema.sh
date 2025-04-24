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

SQLITEVTABDBPATH=$SQLITEVTABDBSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    SQLITEVTABDBPATH=$SQLITEVTABDBHDDPATH
elif [ $DISK = "mem" ]; then
    SQLITEVTABDBPATH=$SQLITEVTABDBMEMPATH
fi
shift

"$SQLITEVTABEXEC" "$SQLITEVTABDBPATH/$DATAB".db < "$SQLITEVTABSCRIPTS"/sqlitevtab_schema.sql;
