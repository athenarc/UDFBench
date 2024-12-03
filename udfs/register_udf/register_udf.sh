#!/bin/bash



# Check if the correct number of arguments is provided
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <system> <database> <disk> "
    exit 1
fi

SYSTEM="$1"
if  [ "$SYSTEM" != "postgres" ] && [ "$SYSTEM" != "monetdb" ] ; then
    echo "Invalid system. Please specify 'monetdb' or 'postgres'."
    exit 1
fi
shift


# SQLite database file
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
PSQLPORT=$PSQLSSDPORT

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    MONETDBPORT=$MONETDBHDDPORT
    PSQLPORT=$PSQLHDDPORT
elif [ $DISK = "mem" ]; then
    MONETDBPORT=$MONETDBMEMPORT
    PSQLPORT=$PSQLMEMPORT
fi
shift


    case "$SYSTEM" in
        postgres)
            export CURRENT=$PWD
            cd ../scalar/postgres;./postgres_scalar.sh; cd $CURRENT;
            $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" < postgres_register_udf.sql
            ;;
        monetdb)
            $MONETDBPATH -p $MONETDBPORT -d "$DATAB"  -t performance --interactive < monetdb_register_udf.sql;
            ;;
        *)
            echo "Unsupported system: $SYSTEM"
            exit 1
            ;;
    esac
