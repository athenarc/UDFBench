#(parameters: s|m|l - duckdb|monetdb|postgres|sqlite -ssd|hdd|mem) ** creates schema and registers udfs
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

        "$SQLITEEXEC" "$SQLITEDBPATH/$DATAB".db < sqlite_schema.sql;
        ;;
        duckdb)
        "$DUCKDBCLI" "$DUCKDBPATH/$DATAB".db < duckdb_schema.sql;
        ;;
        postgres)
            $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" < postgres_schema.sql
            ;;
        monetdb)
            $MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance < monetdb_schema.sql;
            ;;
        *)
            echo "Unsupported system: $SYSTEM"
            exit 1
            ;;
    esac
