#!/bin/bash


# Check if the correct number of arguments is provided
if [ "$#" -lt 8 ]; then
    echo "Usage: $0 <database_file> <threads> <cache> <disk> <collectl> <externalpath> <pythonexec> <query_file1> [<query_file2> ...]"
    exit 1
fi


DATABASE="$1"
shift


if [ ! -d "$RAYRESULTSPATH" ]; then
    mkdir -p "$RAYRESULTSPATH"
    mkdir -p "$RAYRESULTSPATH/experiments"
    mkdir -p "$RAYRESULTSPATH/collectl"
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
    sudo rm -rf "$RAYQUERIES/__pycache__"
    sudo rm -rf "$RAYSCRIPTS/__pycache__"
    sudo rm -rf "$RAYUDFS/scalar/__pycache__"
    sudo rm -rf "$RAYUDFS/aggregate/__pycache__"
    sudo rm -rf "$RAYUDFS/table/__pycache__" 
    # if [ ! -z "$RAYTEMPDIR" ]; then
    #     sudo rm -r "$RAYTEMPDIR/*"
    # fi
    sudo swapoff -a
    sudo swapon -a

    repeats=1
  fi
  for ((i = 1; i <= $repeats; i++)); do
    query_number="${query_file##*/q}"
    query_number="${query_number%.py}"
    filename="ray-$DATABASE"-"$query_number"-t"$NTHREADS"-"$CACHE"-"$DISK"
    rm_output=$(rm -r "$RAYRESULTSPATH/collectl/$filename"* 2>&1)

    

    if  [ $COLLECTL = "true" ]; then 
        collectl -f "$RAYRESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
        COLLECTL_PID=$!
    fi

    if [ $NTHREADS -eq 0 ]; then
        { "$PYTHONEXEC" "$RAYBEXEC" --ray-parquet "$PARQUETPATH/$DATAB" --temp-dir "$RAYTEMPDIR"  --ray-external "$EXTERNALPATH/$DATAB"  --ray-query "$query_number" ; } &> "$RAYRESULTSPATH/experiments/$filename.txt"
    else
        { "$PYTHONEXEC" "$RAYBEXEC"  --ray-parquet "$PARQUETPATH/$DATAB"   --temp-dir "$RAYTEMPDIR"    --ray-external "$EXTERNALPATH/$DATAB" --ray-query "$query_number" --nthreads $NTHREADS ; } &> "$RAYRESULTSPATH/experiments/$filename.txt"
    fi
    if  [ $COLLECTL = "true" ]; then 
        kill $COLLECTL_PID
    fi
done
    if  [ $COLLECTL = "true" ]; then 
        collectl -p $RAYRESULTSPATH/collectl/$filename*.gz -scdnm -P  > $RAYRESULTSPATH/collectl/$filename.csv
    fi

   
done
