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

MONETDBPORT=$MONETDBSSDPORT

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    MONETDBPORT=$MONETDBHDDPORT
elif [ $DISK = "mem" ]; then
    MONETDBPORT=$MONETDBMEMPORT
fi
shift




SQL_DIRS=("$MONETDBUDFS/scalar" "$MONETDBUDFS/aggregate" "$MONETDBUDFS/table")

for dir in "${SQL_DIRS[@]}"; do

    for file in "$dir"/*.sql; do
        $MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance <"$file"
    done
done

sed -i.bak "s|[^']*\.csv'|"$DATASETPATH/csvs/$DATAB"/&|g" "$MONETDBSCRIPTS"/monetdb_load.sql;

$MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance < "$MONETDBSCRIPTS"/monetdb_load.sql;

mv "$MONETDBSCRIPTS"/monetdb_load.sql.bak "$MONETDBSCRIPTS"/monetdb_load.sql;
