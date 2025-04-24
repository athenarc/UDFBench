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

PSQLPORT=$PSQLSSDPORT

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
 
    PSQLPORT=$PSQLHDDPORT
elif [ $DISK = "mem" ]; then
  
    PSQLPORT=$PSQLMEMPORT
fi



export CURRENT=$PWD
cd $POSTGRESUDFS/scalar/extractmonth_c;make; make install; cd $CURRENT;


SQL_DIRS=("$POSTGRESUDFS/scalar" "$POSTGRESUDFS/aggregate" "$POSTGRESUDFS/table")

for dir in "${SQL_DIRS[@]}"; do

    for file in "$dir"/*.sql; do
        $PSQLPATH -U "$PSQLUSER" -p "$PSQLPORT" "$DATAB" -f "$file"
    done
done

sed -i.bak "s|[^']*\.csv'|"$DATASETPATH/csvs/$DATAB"/&|g" "$POSTGRESSCRIPTS"/postgres_load.sql;

$PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$POSTGRESSCRIPTS"/postgres_load.sql;

mv "$POSTGRESSCRIPTS"/postgres_load.sql.bak "$POSTGRESSCRIPTS"/postgres_load.sql;
