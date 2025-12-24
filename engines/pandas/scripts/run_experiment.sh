#!/bin/bash

# Check if the correct number of arguments is provided

if [ "$#" -lt 8 ]; then
    echo "Usage: $0 <database_file> <threads> <cache> <disk> <collectl> <externalpath> <pythonexec> <query_file1> [<query_file2> ...]"
    exit 1
fi
DATABASE="$1"
shift


if [ ! -d "$PANDASRESULTSPATH" ]; then
    mkdir -p "$PANDASRESULTSPATH"
    mkdir -p "$PANDASRESULTSPATH/experiments"
    mkdir -p "$PANDASRESULTSPATH/collectl"
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

if [ "$NTHREADS" -gt 0 ]; then
    export MODIN_CPUS=$NTHREADS
fi

shift
CACHE="$1"
shift
DISK="$1"


PANDASPATH=$PANDASSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    PANDASPATH=$PANDASPATHHDD
elif [ $DISK = "mem" ]; then
    PANDASPATH=$PANDASPATHMEM
fi

if [ $PANDASDATAFORMAT = "csv" ]; then 
    PANDASDATAPATH="$PANDASPATH/csvs/$DATAB"
elif [ $PANDASDATAFORMAT = "parquet" ]; then 
    PANDASDATAPATH="$PANDASPATH/parquet/$DATAB"
else
    echo "Unsupported Pandas-like system data format: $PANDASDATAFORMAT"
    exit 1
fi
shift

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
        sudo rm -rf "$PANDASQUERIES/__pycache__"
        sudo rm -rf "$PANDASSCRIPTS/__pycache__"
        sudo rm -rf "$PANDASSCALAR/__pycache__"
        sudo rm -rf "$PANDASAGGR/__pycache__"
        sudo rm -rf "$PANDASTABLE/__pycache__"        
        sudo swapoff -a
        sudo swapon -a

        repeats=1
    fi
    for ((i = 1; i <= $repeats; i++)); do
        query_number="${query_file##*/q}"
        query_number="${query_number%.py}"
        filename="$DFENGINE"-"$DATABASE"-"$query_number"-t"$NTHREADS"-"$CACHE"-"$DISK"
        rm_output=$(rm -r "$PANDASRESULTSPATH/collectl/$filename"* 2>&1)

        if [ $COLLECTL = "true" ]; then 
            collectl -f "$PANDASRESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
            COLLECTL_PID=$!
        fi

        
        { "$PYTHONEXEC" "$PANDASEXEC" "$DFENGINE" "$PANDASSCHEMA" "$PANDASDATAPATH" "$PANDASDATAFORMAT" "$EXTERNALPATH/$DATAB" "$query_file" "$PANDASSCALAR" "$PANDASAGGR" "$PANDASTABLE"; } &> "$PANDASRESULTSPATH/experiments/$filename".txt

        if  [ $COLLECTL = "true" ]; then 
            kill $COLLECTL_PID
        fi
       
    done
    if  [ $COLLECTL = "true" ]; then 
        collectl -p $PANDASRESULTSPATH/collectl/$filename*.gz -scdnm -P  > $PANDASRESULTSPATH/collectl/$filename.csv
    fi
done
