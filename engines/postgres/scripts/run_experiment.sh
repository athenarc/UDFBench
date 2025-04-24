#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -lt 8 ]; then
    echo "Usage: $0 <database_file> <threads> <cache> <disk> <collectl> <externalpath> <pythonexec> <query_file1> [<query_file2> ...]"
    exit 1
fi

DATABASE="$1"
shift


if [ ! -d "$POSTGRESRESULTSPATH" ]; then
    mkdir -p "$POSTGRESRESULTSPATH"
    mkdir -p "$POSTGRESRESULTSPATH/experiments"
    mkdir -p "$POSTGRESRESULTSPATH/collectl"
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

PSQLPORT=$PSQLSSDPORT

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    PSQLPORT=$PSQLHDDPORT
elif [ $DISK = "mem" ]; then
    PSQLPORT=$PSQLMEMPORT
fi


COLLECTL="$1"
shift

EXTERNALPATH="$1"
shift

PYTHONEXEC="$1"
shift

arr=("$@")

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
    rm_output=$(rm -r "$POSTGRESRESULTSPATH/collectl/$filename"* 2>&1)

    sed -i.bak -e "s|[^']*\.txt'|"$EXTERNALPATH/$DATAB"/&|g" \
    -e "s|[^']*\.csv'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.xml'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.json'|"$EXTERNALPATH/$DATAB"/&|g" "$query_file"
    
    PNTHREADS=$((NTHREADS - 1))

    if  [ $COLLECTL = "true" ]; then 
        collectl -f "$POSTGRESRESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
        COLLECTL_PID=$!
    fi
    
    if [ $PNTHREADS -eq -1 ]; then
        $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$query_file"  > "$POSTGRESRESULTSPATH/experiments/$filename".txt
    else
        $PSQLPATH -U "$PSQLUSER" -p "$PSQLPORT" -d "$DATAB" -c "SET max_parallel_workers = $PNTHREADS; SET  max_parallel_workers_per_gather = $PNTHREADS;" -f "$query_file" > "$POSTGRESRESULTSPATH/experiments/$filename.txt"
    fi
    
    if  [ $COLLECTL = "true" ]; then 
        kill $COLLECTL_PID
    fi
    mv "$query_file.bak" "$query_file"

done
    if  [ $COLLECTL = "true" ]; then 
        collectl -p $POSTGRESRESULTSPATH/collectl/$filename*.gz -scdnm -P  > $POSTGRESRESULTSPATH/collectl/$filename.csv
    fi
    if [[ $query_number == '20' ]] && (( repeats % 2 != 0 )); then
        $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$query_file" &>/dev/null
    elif [[ $query_number == '21' ]]; then
        $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -c "delete from projects_artifacts where provenance='crossref'" &>/dev/null
    fi
   
done
