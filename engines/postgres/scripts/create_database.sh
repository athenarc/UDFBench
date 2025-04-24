#!/bin/bash

export CURRENT=$PWD
export POSTPATH=$POSTGRESPATH

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

PSQLPORT=$PSQLSSDPORT

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then

    PSQLPORT=$PSQLHDDPORT
elif [ $DISK = "mem" ]; then
    PSQLPORT=$PSQLMEMPORT
fi
shift

$POSTPATH/bin/psql -U "$PSQLUSER" -p "$PSQLPORT" -d postgres  -tc "SELECT 1 FROM pg_database WHERE datname = '$DATAB'" | grep -q 1 ||  $POSTPATH/bin/createdb -U $PSQLUSER -p $PSQLPORT $DATAB

