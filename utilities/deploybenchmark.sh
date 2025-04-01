#parameters: s|m|l - duckdb|monetdb|postgres|sqlite3 -ssd|hdd|mem

#!/bin/bash

# source $PWD'/utilities/config.sh'
export CURRENT=$PWD

# Check if the correct number of arguments is provided
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <system> <database> <disk> "
    exit 1
fi

SYSTEM="$1"
if [ "$SYSTEM" != "sqlite3" ] && [ "$SYSTEM" != "postgres" ] && [ "$SYSTEM" != "monetdb" ] && [ "$SYSTEM" != "duckdb" ] && [ "$SYSTEM" != "pyspark" ] ; then
    echo "Invalid system. Please specify 'sqlite', 'postgres','monetdb','pyspark' or 'duckdb'."
    exit 1
fi
shift


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

cd $CURRENT'/schema'
./create_schema.sh $SYSTEM $DATABASE $DISK

cd $CURRENT'/dataset/load_scripts'
./load.sh $SYSTEM $DATABASE $DISK


case "$SYSTEM" in
    sqlite3)
    :
    ;;
    duckdb)
    :
    ;;
    pyspark)
        cd $CURRENT'/udfs/register_udf';
        ./register_udf.sh $SYSTEM $DATABASE $DISK
        ;;
    postgres)
        cd $CURRENT'/udfs/register_udf';
        ./register_udf.sh $SYSTEM $DATABASE $DISK
        ;;
    monetdb)
        cd $CURRENT'/udfs/register_udf';
        ./register_udf.sh $SYSTEM $DATABASE $DISK
        ;;
    *)
        echo "Unsupported system: $SYSTEM"
        exit 1
        ;;
esac

cd $CURRENT