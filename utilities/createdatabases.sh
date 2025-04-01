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
if [ "$SYSTEM" != "sqlite3" ] && [ "$SYSTEM" != "postgres" ] && [ "$SYSTEM" != "monetdb" ] && [ "$SYSTEM" != "duckdb" ] && [ "$SYSTEM" != "pyspark" ]; then
    echo "Invalid system. Please specify 'sqlite', 'postgres','monetdb', 'pyspark' or 'duckdb'."
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

SQLITEDBPATH=$SQLITEDBSSDPATH
MONETDBPORT=$MONETDBSSDPORT
PSQLPORT=$PSQLSSDPORT
DUCKDBPATH=$DUCKDBSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    SQLITEDBPATH=$SQLITEDBHDDPATH
    MONETDBPORT=$MONETDBHDDPORT
    PSQLPORT=$PSQLHDDPORT
    DUCKDBPATH=$DUCKDBHDDPATH
elif [ $DISK = "mem" ]; then
    SQLITEDBPATH=$SQLITEDBMEMPATH
    MONETDBPORT=$MONETDBMEMPORT
    PSQLPORT=$PSQLMEMPORT
    DUCKDBPATH=$DUCKDBMEMPATH
fi
shift

case "$SYSTEM" in
    sqlite3)
        touch "$SQLITEDBPATH/$DATAB".db
        ;;
    duckdb)
        # "$DUCKDBCLI" "$DUCKDBPATH/$DATAB".db 
        :
        ;;
    pyspark)
        :
        ;;
    postgres)

        $POSTPATH/bin/psql -U "$PSQLUSER" -p "$PSQLPORT" -d postgres  -tc "SELECT 1 FROM pg_database WHERE datname = '$DATAB'" | grep -q 1 ||  $POSTPATH/bin/createdb -U $PSQLUSER -p $PSQLPORT $DATAB
        ;;
    monetdb)
        DATABASE_STATUS=$("$MONETDBBINPATH/monetdb" status "$DATAB" 2>&1)

        if echo "$DATABASE_STATUS" | grep -q "no such database"; then
            
            $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT create $DATAB
            $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT set embedc=true $DATAB
            $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT set embedpy3=true $DATAB
            $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT release $DATAB
            $MONETDBDIRPATH/bin/monetdb -p $MONETDBPORT start $DATAB
               
        fi

        ;;
    *)
        echo "Unsupported system: $SYSTEM"
        exit 1
        ;;
esac
