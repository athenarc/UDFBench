#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -lt 8 ]; then
    echo "Usage: $0 <database_file> <threads> <cache> <disk> <collectl> <externalpath> <pythonexec> <query_file1> [<query_file2> ...]"
    exit 1
fi

DATABASE="$1"
shift


if [ ! -d "$DUCKDBRESULTSPATH" ]; then
    mkdir -p "$DUCKDBRESULTSPATH"
    mkdir -p "$DUCKDBRESULTSPATH/experiments"
    mkdir -p "$DUCKDBRESULTSPATH/collectl"
fi

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

NTHREADS="$1"

shift
CACHE="$1"
shift
DISK="$1"
shift


DUCKDBPATH=$DUCKDBSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    DUCKDBPATH=$DUCKDBHDDPATH
elif [ $DISK = "mem" ]; then
    DUCKDBPATH=$DUCKDBMEMPATH
fi


COLLECTL="$1"
shift

EXTERNALPATH="$1"
shift

PYTHONEXEC="$1"
shift

arr=("$@")

# Iterate over each element in the array
for query_file in "${arr[@]}"; do

  repeats=1
  if [ $CACHE = "hot" ]; then
    repeats=2
  else

    sudo sync; sudo sh -c 'echo 1 > /proc/sys/vm/drop_caches'
    sudo sync; sudo sh -c 'echo 2 > /proc/sys/vm/drop_caches'
    sudo sync; sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
    echo 3 | sudo  tee /proc/sys/vm/drop_caches
    sudo swapoff -a
    sudo swapon -a

    repeats=1
  fi
  for ((i = 1; i <= $repeats; i++)); do
    query_number="${query_file##*/q}"
    query_number="${query_number%.sql}"
    filename="$DATABASE"-"$query_number"-t"$NTHREADS"-"$CACHE"-"$DISK"
    rm_output=$(rm -r "$DUCKDBRESULTSPATH/collectl/$filename"* 2>&1)

    if  [ $COLLECTL = "true" ]; then 
        collectl -f "$DUCKDBRESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
        COLLECTL_PID=$!
    fi
    if [ $NTHREADS -eq 0 ]; then
        { "$PYTHONEXEC" "$DUCKDBEXEC" --duckdb-dbfile "$DUCKDBPATH/$DATAB".db  --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/$DATAB" --duckdb-sql "$query_file" ; } &> "$DUCKDBRESULTSPATH/experiments/$filename.txt"
    else
        { "$PYTHONEXEC" "$DUCKDBEXEC" --duckdb-dbfile "$DUCKDBPATH/$DATAB".db  --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/$DATAB" --duckdb-sql "$query_file" --nthreads $NTHREADS ; } &> "$DUCKDBRESULTSPATH/experiments/$filename.txt"
    fi
    if  [ $COLLECTL = "true" ]; then 
        kill $COLLECTL_PID
    fi
    
done
    if  [ $COLLECTL = "true" ]; then 
        collectl -p $DUCKDBRESULTSPATH/collectl/$filename*.gz -scdnm -P  > $DUCKDBRESULTSPATH/collectl/$filename.csv
    fi
    if [[ $query_number == '20' ]] && (( repeats % 2 != 0 )); then

        "$PYTHONEXEC" "$DUCKDBEXEC" --duckdb-dbfile "$DUCKDBPATH/$DATAB".db  --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/$DATAB" --duckdb-sql "$query_file" &>/dev/null
    elif [[ $query_number == '21' ]]; then
        tmpfile=$(mktemp "$DUCKDBSCRIPTS/q21_revert.XXXXXX.sql")

        cat <<EOF > "$tmpfile"
DELETE FROM projects_artifacts WHERE provenance = 'crossref';
EOF
        "$PYTHONEXEC" "$DUCKDBEXEC" --duckdb-dbfile "$DUCKDBPATH/$DATAB".db  --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/$DATAB" --duckdb-sql "$tmpfile"  &>/dev/null
        rm "$tmpfile"

    fi
   
done
