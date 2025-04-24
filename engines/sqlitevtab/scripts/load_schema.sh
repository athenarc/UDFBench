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


SQLITEVTABDBPATH=$SQLITEVTABDBSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    SQLITEVTABDBPATH=$SQLITEVTABDBHDDPATH
elif [ $DISK = "mem" ]; then
    SQLITEVTABDBPATH=$SQLITEVTABDBMEMPATH
fi
shift


sed -i.bak "s|[^']*\.csv'|"$DATASETPATH/csvs/$DATAB"/&|g" "$SQLITEVTABSCRIPTS"/sqlitevtab_load.sql;

"$SQLITEVTABEXEC" "$SQLITEVTABDBPATH/$DATAB".db  < "$SQLITEVTABSCRIPTS"/sqlitevtab_load.sql;

mv "$SQLITEVTABSCRIPTS"/sqlitevtab_load.sql.bak "$SQLITEVTABSCRIPTS"/sqlitevtab_load.sql
