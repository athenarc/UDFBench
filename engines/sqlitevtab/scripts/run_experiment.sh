#!/bin/bash


# Check if the correct number of arguments is provided
if [ "$#" -lt 8 ]; then
    echo "Usage: $0 <database_file> <threads> <cache> <disk> <collectl> <externalpath> <pythonexec> <query_file1> [<query_file2> ...]"
    exit 1
fi

DATABASE="$1"
shift


if [ ! -d "$SQLITEVTABRESULTSPATH" ]; then
    mkdir -p "$SQLITEVTABRESULTSPATH"
    mkdir -p "$SQLITEVTABRESULTSPATH/experiments"
    mkdir -p "$SQLITEVTABRESULTSPATH/collectl"
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

SQLITEVTABDBPATH=$SQLITEVTABDBSSDPATH

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    SQLITEVTABDBPATH=$SQLITEVTABDBHDDPATH
elif [ $DISK = "mem" ]; then
    SQLITEVTABDBPATH=$SQLITEVTABDBMEMPATH
fi



COLLECTL="$1"
shift

EXTERNALPATH="$1"
shift

PYTHONEXEC="$1"
shift

cp  $SQLITEVTABUDFS/scalar/*.py $SQLITEVTABFUNCTIONS/row
cp  $SQLITEVTABUDFS/aggregate/*.py $SQLITEVTABFUNCTIONS/aggregate
cp  $SQLITEVTABUDFS/table/*.py $SQLITEVTABFUNCTIONS/vtable

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
    rm_output=$(rm -r "$SQLITEVTABRESULTSPATH/collectl/$filename"* 2>&1)


    sed -i.bak -e "s|[^']*\.txt'|"$EXTERNALPATH/$DATAB"/&|g" \
    -e "s|[^']*\.csv'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.xml'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.json'|"$EXTERNALPATH/$DATAB"/&|g" "$query_file"
    
    if [ $COLLECTL = "true" ]; then 
        collectl -f "$SQLITEVTABRESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
        COLLECTL_PID=$!
    fi
    { "$PYTHONEXEC" "$SQLITEVTABPATH" -d "$SQLITEVTABDBPATH/$DATAB".db -f "$query_file"; } &> "$SQLITEVTABRESULTSPATH/experiments/$filename".txt
    if  [ $COLLECTL = "true" ]; then 
        kill $COLLECTL_PID
    fi

    mv "$query_file.bak" "$query_file"

       
done
    if  [ $COLLECTL = "true" ]; then 
        collectl -p $SQLITEVTABRESULTSPATH/collectl/$filename*.gz -scdnm -P  > $SQLITEVTABRESULTSPATH/collectl/$filename.csv
    fi
    if [[ $query_number == '20' ]] && (( repeats % 2 != 0 )); then

        "$PYTHONEXEC" "$SQLITEVTABPATH"  "$SQLITEVTABDBPATH/$DATAB".db  -f "$query_file"  &>/dev/null

    elif [[ $query_number == '21' ]]; then
        tmpfile=$(mktemp "$SQLITEVTABSCRIPTS/q21_revert.XXXXXX.sql")

        cat <<EOF > "$tmpfile"
DELETE FROM projects_artifacts WHERE provenance = 'crossref';
EOF
        "$PYTHONEXEC" "$SQLITEVTABPATH" -d "$SQLITEVTABDBPATH/$DATAB".db -f "$tmpfile" &>/dev/null

        rm "$tmpfile"

    fi
   
done
