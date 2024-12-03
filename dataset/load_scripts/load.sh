#!/bin/bash



# Check if the correct number of arguments is provided
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <system> <database> <disk> "
    exit 1
fi

SYSTEM="$1"
if [ "$SYSTEM" != "sqlite3" ] && [ "$SYSTEM" != "postgres" ] && [ "$SYSTEM" != "monetdb" ] && [ "$SYSTEM" != "duckdb" ]; then
    echo "Invalid system. Please specify 'sqlite' or 'postgres'."
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
            sed -i.bak "s|[^']*\.csv'|"$CSVSPATH/$DATAB"/&|g" sqlite_load.sql;
            "$SQLITEEXEC" "$SQLITEDBPATH/$DATAB".db < sqlite_load.sql
            # "$PYPYPATH" "$SCRIPTPATH" -d "$SQLITEDBPATH/$DATAB".db < sqlite_load.sql;
            mv sqlite_load.sql.bak sqlite_load.sql;
            ;;
        duckdb)
            sed -i.bak "s|[^']*\.csv'|"$CSVSPATH/$DATAB"/&|g" duckdb_load.sql;
            "$DUCKDBCLI" "$DUCKDBPATH/$DATAB".db < duckdb_load.sql;
            mv duckdb_load.sql.bak duckdb_load.sql;
            ;;
        postgres)
            sed -i.bak "s|[^']*\.csv'|"$CSVSPATH/$DATAB"/&|g" postgres_load.sql;

            $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f postgres_load.sql;
            mv postgres_load.sql.bak postgres_load.sql;
            ;;
        monetdb)
            sed -i.bak "s|[^']*\.csv'|"$CSVSPATH/$DATAB"/&|g" monetdb_load.sql;
            $MONETDBPATH -p $MONETDBPORT -d "$DATAB" -t performance < monetdb_load.sql;
            mv monetdb_load.sql.bak monetdb_load.sql;
            ;;
        *)
            echo "Unsupported system: $SYSTEM"
            exit 1
            ;;
    esac
