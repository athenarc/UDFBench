#!/bin/bash

# echo "Skipping Schema loading for Polars."

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


POLARSPATH=$POLARSSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    POLARSPATH=$POLARSPATHHDD
elif [ $DISK = "mem" ]; then
    POLARSPATH=$POLARSPATHMEM
fi


DATASETPATH="$1"
shift

if [ $POLARSDATAFORMAT = "csv" ]; then 
    DATAFORMAT="csvs"
elif [ $POLARSDATAFORMAT = "parquet" ]; then 
    DATAFORMAT="parquet"
else
    echo "Unsupported Polars-like system data format: $POLARSDATAFORMAT"
    exit 1
fi
mkdir -p  "$POLARSPATH";
mkdir -p  "$POLARSPATH/$DATAFORMAT";

cp -r "$DATASETPATH/$DATAFORMAT/$DATAB" "$POLARSPATH"/$DATAFORMAT/"$DATAB"/;