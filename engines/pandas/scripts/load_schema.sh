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


PANDASPATH=$PANDASSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    PANDASPATH=$PANDASPATHHDD
elif [ $DISK = "mem" ]; then
    PANDASPATH=$PANDASPATHMEM
fi


DATASETPATH="$1"
shift

if [ $PANDASDATAFORMAT = "csv" ]; then 
    DATAFORMAT="csvs"
elif [ $PANDASDATAFORMAT = "parquet" ]; then 
    DATAFORMAT="parquet"
else
    echo "Unsupported Pandas-like system data format: $PANDASDATAFORMAT"
    exit 1
fi
mkdir -p  "$PANDASPATH";
mkdir -p  "$PANDASPATH/$DATAFORMAT";

cp -r "$DATASETPATH/$DATAFORMAT/$DATAB" "$PANDASPATH"/$DATAFORMAT/"$DATAB"/;