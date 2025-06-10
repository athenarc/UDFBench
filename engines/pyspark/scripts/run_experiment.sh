#!/bin/bash


# Check if the correct number of arguments is provided
if [ "$#" -lt 8 ]; then
    echo "Usage: $0 <database_file> <threads> <cache> <disk> <collectl> <externalpath> <pythonexec> <query_file1> [<query_file2> ...]"
    exit 1
fi


DATABASE="$1"
shift


if [ ! -d "$PYSPARKRESULTSPATH" ]; then
    mkdir -p "$PYSPARKRESULTSPATH"
    mkdir -p "$PYSPARKRESULTSPATH/experiments"
    mkdir -p "$PYSPARKRESULTSPATH/collectl"
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

PARQUETPATH=$PARQUETPATHSSD

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    PARQUETPATH=$PARQUETPATHHDD
elif [ $DISK = "mem" ]; then
    PARQUETPATH=$PARQUETPATHMEM
fi

shift

COLLECTL="$1"
shift

EXTERNALPATH="$1"
shift

PYTHONEXEC="$1"
shift

export PYSPARK_DRIVER_PYTHON=$PYTHONEXEC
export PYSPARK_PYTHON=$PYTHONEXEC

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
    rm_output=$(rm -r "$PYSPARKRESULTSPATH/collectl/$filename"* 2>&1)

    sed -i.bak -e "s|[^']*\.txt'|"$EXTERNALPATH/$DATAB"/&|g" \
    -e "s|[^']*\.csv'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.xml'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.json'|"$EXTERNALPATH/$DATAB"/&|g" "$query_file"
    


    if  [ $COLLECTL = "true" ]; then 
        collectl -f "$PYSPARKRESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
        COLLECTL_PID=$!
    fi
    "$PYTHONEXEC" "$PYSPARKPATH" --pyspark-schema "$PYSPARKSCRIPTS" --pyspark-loads "$PYSPARKSCRIPTS" --pyspark-parquet "$PARQUETPATH/$DATAB" --pyspark-udfs "$PYSPARKUDFS"  --pyspark-sql  "$query_file"  &> "$PYSPARKRESULTSPATH/experiments/$filename".txt
    if  [ $COLLECTL = "true" ]; then 
        kill $COLLECTL_PID
    fi
    mv "$query_file.bak" "$query_file"

    
done
    if  [ $COLLECTL = "true" ]; then 
        collectl -p $PYSPARKRESULTSPATH/collectl/$filename*.gz -scdnm -P  > $PYSPARKRESULTSPATH/collectl/$filename.csv
    fi

   
done
