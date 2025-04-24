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

PARQUETPATH=$PARQUETPATHSSD

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    PARQUETPATH=$PARQUETPATHHDD
elif [ $DISK = "mem" ]; then
    PARQUETPATH=$PARQUETPATHMEM
fi

shift

DATASETPATH="$1"
shift

mkdir -p  "$PARQUETPATH";

cp -r "$DATASETPATH/parquet/$DATAB" "$PARQUETPATH"/"$DATAB"/;

export CURRENT=$PWD
cd $PYSPARKUDFS/scalar/extractmonth_java; mvn clean; mvn clean package; cd $CURRENT;

cd $PYSPARKUDFS/scalar/extractday_scala; mvn clean; mvn clean package; cd $CURRENT;


