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

PSQLPORT=$PSQLSSDPORT

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    PSQLPORT=$PSQLHDDPORT
elif [ $DISK = "mem" ]; then
    PSQLPORT=$PSQLMEMPORT
fi
shift

$PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" < "$POSTGRESSCRIPTS"/postgres_schema.sql
       