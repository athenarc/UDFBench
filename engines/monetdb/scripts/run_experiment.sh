#!/bin/bash
cores=$(nproc)
# Check if the correct number of arguments is provided
if [ "$#" -lt 8 ]; then
    echo "Usage: $0 <database_file> <threads> <cache> <disk> <collectl> <externalpath> <pythonexec> <query_file1> [<query_file2> ...]"
    exit 1
fi


DATABASE="$1"
shift

if [ ! -d "$MONETDBRESULTSPATH" ]; then
    mkdir -p "$MONETDBRESULTSPATH"
    mkdir -p "$MONETDBRESULTSPATH/experiments"
    mkdir -p "$MONETDBRESULTSPATH/collectl"
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


MONETDBPORT=$MONETDBSSDPORT

if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    MONETDBPORT=$MONETDBHDDPORT
elif [ $DISK = "mem" ]; then
    MONETDBPORT=$MONETDBMEMPORT
fi
shift




COLLECTL="$1"
shift

EXTERNALPATH="$1"
shift

PYTHONEXEC="$1"
shift


arr=("$@")


if [ $NTHREADS -gt  0 ];then
    DEFAULT_THREADS=$($MONETDBBINPATH/monetdb -p $MONETDBPORT get nthreads "$DATAB" | awk 'NR==2 {print $4}')
    $MONETDBBINPATH/monetdb -p $MONETDBPORT  stop "$DATAB"
    $MONETDBBINPATH/monetdb -p $MONETDBPORT  set nthreads=$NTHREADS "$DATAB"
    $MONETDBBINPATH/monetdb -p $MONETDBPORT  start "$DATAB"
fi


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
    rm_output=$(rm -r "$MONETDBRESULTSPATH/collectl/$filename"* 2>&1)

    sed -i.bak -e "s|[^']*\.txt'|"$EXTERNALPATH/$DATAB"/&|g" \
    -e "s|[^']*\.csv'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.xml'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.json'|"$EXTERNALPATH/$DATAB"/&|g" "$query_file"
    
    PNTHREADS=$((NTHREADS - 1))

    if  [ $COLLECTL = "true" ]; then 
        collectl -f "$MONETDBRESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
        COLLECTL_PID=$!
    fi
    
    { $MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance < "$query_file"; } 2> "$MONETDBRESULTSPATH/experiments/$filename".txt

    if  [ $COLLECTL = "true" ]; then 
        kill $COLLECTL_PID
    fi
    mv "$query_file.bak" "$query_file"

done
    if  [ $COLLECTL = "true" ]; then 
        collectl -p $MONETDBRESULTSPATH/collectl/$filename*.gz -scdnm -P  > $MONETDBRESULTSPATH/collectl/$filename.csv
    fi
    if [[ $query_number == '20' ]] && (( repeats % 2 != 0 )); then
        $MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance < "$query_file" &>/dev/null
    elif [[ $query_number == '21' ]]; then
        $MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance -e "delete from projects_artifacts where provenance='crossref'" &>/dev/null
    fi
    "$MONETDBSCRIPTS"/format_time.sh "$MONETDBRESULTSPATH/experiments/$filename".txt
   
done
if  [ $NTHREADS -gt  0 ];then
    $MONETDBBINPATH/monetdb -p $MONETDBPORT  stop "$DATAB"
    if [[ -n $DEFAULT_THREADS ]];then
        $MONETDBBINPATH/monetdb -p $MONETDBPORT  set nthreads=$DEFAULT_THREADS "$DATAB"
    else
        $MONETDBBINPATH/monetdb -p $MONETDBPORT  set nthreads=$cores "$DATAB"
    fi
    $MONETDBBINPATH/monetdb -p $MONETDBPORT  start "$DATAB"
fi