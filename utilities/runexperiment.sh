#!/bin/bash

cores=$(nproc)
# Check if the correct number of arguments is provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <database_file> <query_file1> [<query_file2> ...]"
    exit 1
fi

SYSTEM="$1"
if [ "$SYSTEM" != "sqlite3" ] && [ "$SYSTEM" != "sqlitevtab" ] && [ "$SYSTEM" != "postgres" ] && [ "$SYSTEM" != "monetdb" ] && [ "$SYSTEM" != "duckdb" ] && [ "$SYSTEM" != "duckdbpandas" ]; then
    echo "Invalid system. Please specify 'sqlite' or 'postgres'."
    exit 1
fi
shift


# SQLite database file
DATABASE="$1"
shift


if [ ! -d "$RESULTSPATH" ]; then
    mkdir -p "$RESULTSPATH"
    mkdir -p "$RESULTSPATH/script"
    mkdir -p "$RESULTSPATH/collectl"
    touch "$RESULTSPATH/collectl/collectls.db"
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

THREADS="$1"
NTHREADS=$(echo "$THREADS" | grep -oE '[0-9]+')

shift
CACHE="$1"
shift
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

WORKLOAD="$1"
shift


COLLECTL="$1"
shift

echo "$NTHREADS" "$DATAB" "$CACHE" "$DISK" "$WORKLOAD"
if [ "$SYSTEM" = "monetdb" ]  &&  [ $NTHREADS -gt  0 ];then
            DEFAULT_THREADS=$("$MONETDBBINPATH/monetdb -p $MONETDBPORT get nthreads "$DATAB"" | awk 'NR==2 {print $4}')
            # echo $DEFAULT_THREADS
            $MONETDBBINPATH/monetdb -p $MONETDBPORT  stop "$DATAB"
            $MONETDBBINPATH/monetdb -p $MONETDBPORT  set nthreads=$NTHREADS "$DATAB"
            $MONETDBBINPATH/monetdb -p $MONETDBPORT  start "$DATAB"
fi
if  [ $WORKLOAD = "true" ]; then
# TODO
    for query_file in "$@"; do
        sed -i.bak -e "s|[^']*\.txt'|"$EXTERNALPATH/$DATAB"/&|g" \
        -e "s|[^']*\.csv'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.xml'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.json'|"$EXTERNALPATH/$DATAB"/&|g" "$POSTGRESQUERIES/q$query_file.sql"
        $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$POSTGRESQUERIES/q$query_file.sql"  > "$RESULTSPATH/$filename".txt &
        mv "$POSTGRESQUERIES/q$query_file.sql.bak" "$POSTGRESQUERIES/q$query_file.sql"
    done
    wait
elif [ $WORKLOAD = "false" ]; then
for query_file in "$@"; do
  echo $query_file
  repeats=1
  if [ $CACHE = "hot" ]; then
    repeats=2
  else
    # TODO cold cache clean caches, clean also caches in server databases
    # if [ "$SYSTEM" = "monetdb" ] ; then
    #     $MONETDBBINPATH/monetdb -p $MONETDBPORT  stop "$DATAB"
    # fi
    sudo sync; sudo sh -c 'echo 1 > /proc/sys/vm/drop_caches'
    sudo sync; sudo sh -c 'echo 2 > /proc/sys/vm/drop_caches'
    sudo sync; sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
    echo 3 | sudo  tee /proc/sys/vm/drop_caches
    sudo swapoff -a
    sudo swapon -a
    # if [ "$SYSTEM" = "monetdb" ] ; then
    #     $MONETDBBINPATH/monetdb -p $MONETDBPORT  start "$DATAB"
    # fi
    repeats=1
  fi
  for ((i = 1; i <= $repeats; i++)); do
    # rm -r "$RESULTSPATH/collectl/$SYSTEM"-"$DATABASE"-"$query_file"*
    filename="$SYSTEM"-"$DATABASE"-"$query_file"-t"$NTHREADS"-"$CACHE"-"$DISK"
    filenamesql=${SYSTEM}_${DATABASE}_${query_file}_t${NTHREADS}_${CACHE}_$DISK
    rm_output=$(rm -r "$RESULTSPATH/collectl/$filename"* 2>&1)
    filename_parsed="$filename"_parsed

    # Run the query
    case "$SYSTEM" in
        duckdb)
        if  [ $COLLECTL = "true" ]; then 
            collectl -f "$RESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
        fi
        if [ $NTHREADS -eq 0 ]; then
            { "$PYTHONEXEC" "$DUCKPATH" --duckdb-dbfile "$DUCKDBPATH/$DATAB".db  --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/$DATAB" --duckdb-sql "$DUCKDBQUERIES/q$query_file.sql"  ; } &> "$RESULTSPATH/$filename".txt
        else
            { "$PYTHONEXEC" "$DUCKPATH" --duckdb-dbfile "$DUCKDBPATH/$DATAB".db  --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/$DATAB" --duckdb-sql "$DUCKDBQUERIES/q$query_file.sql" --nthreads $NTHREADS ; } &> "$RESULTSPATH/$filename".txt
        fi

        ;;

        sqlitevtab)

        sed -i.bak -e "s|[^']*\.txt'|"$EXTERNALPATH/$DATAB"/&|g" \
        -e "s|[^']*\.csv'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.xml'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.json'|"$EXTERNALPATH/$DATAB"/&|g" "$SQLITEVTABQUERIES/q$query_file.sql"
       

        if [ $COLLECTL = "true" ]; then 
            collectl -f "$RESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
        fi
        { "$PYTHONEXEC" "$SQLITEVTABPATH" -d "$SQLITEDBPATH/$DATAB".db -f "$SQLITEVTABQUERIES/q$query_file.sql"; } &> "$RESULTSPATH/$filename".txt
        
        mv "$SQLITEVTABQUERIES/q$query_file.sql.bak" "$SQLITEVTABQUERIES/q$query_file.sql"
        ;;
        sqlite3)

        if [ $COLLECTL = "true" ]; then 
            collectl -f "$RESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
        fi
        { "$PYTHONEXEC" "$SQLITEPATH"  "$SQLITEDBPATH/$DATAB".db "$SQLITEQUERIES/q$query_file.sql" "$SQLITESCALAR/scalar" "$SQLITEAGGRS/aggrs"; } &> "$RESULTSPATH/$filename".txt

        ;;
        postgres)
        sed -i.bak -e "s|[^']*\.txt'|"$EXTERNALPATH/$DATAB"/&|g" \
        -e "s|[^']*\.csv'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.xml'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.json'|"$EXTERNALPATH/$DATAB"/&|g" "$POSTGRESQUERIES/q$query_file.sql"
       
        PNTHREADS=$((NTHREADS - 1))
        QUERY_THREADS="$RESULTSPATH/script/$filename"-threads.sql
    # Write query init based on the system
        cat <<EOF > "$QUERY_THREADS"
SET  max_parallel_workers = $PNTHREADS;
SET  max_parallel_workers_per_gather = $PNTHREADS;
EOF
        if  [ $COLLECTL = "true" ]; then 
            collectl -f "$RESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
            COLLECTL_PID=$!
        fi
        if [[ $query_file == '20' ]]; then
            if [ $PNTHREADS -eq -1 ]; then
                $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$POSTGRESQUERIES/index.sql" -f "$POSTGRESQUERIES/q$query_file.sql"  > "$RESULTSPATH/$filename".txt
            else
                $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$RESULTSPATH/script/$filename"-threads.sql  -f "$POSTGRESQUERIES/index.sql" -f "$POSTGRESQUERIES/q$query_file.sql"  > "$RESULTSPATH/$filename.txt"

            fi

        else
            if [ $PNTHREADS -eq -1 ]; then
                $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$POSTGRESQUERIES/q$query_file.sql"  > "$RESULTSPATH/$filename".txt
            else
                $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$RESULTSPATH/script/$filename"-threads.sql -f "$POSTGRESQUERIES/q$query_file.sql"  > "$RESULTSPATH/$filename.txt"
            fi
        fi
        if  [ $COLLECTL = "true" ]; then 
            kill $COLLECTL_PID
        fi
        mv "$POSTGRESQUERIES/q$query_file.sql.bak" "$POSTGRESQUERIES/q$query_file.sql"
            ;;
        monetdb)
        sed -i.bak -e "s|[^']*\.txt'|"$EXTERNALPATH/$DATAB"/&|g" \
        -e "s|[^']*\.csv'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.xml'|"$EXTERNALPATH/$DATAB"/&|g" -e "s|[^']*\.json'|"$EXTERNALPATH/$DATAB"/&|g" "$MONETDBQUERIES/q$query_file.sql"
       
        if  [ $COLLECTL = "true" ]; then 
            collectl -f "$RESULTSPATH/collectl/$filename" -scdnm -F0 -i.1 &
            COLLECTL_PID=$!
        fi
        { $MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance < "$MONETDBQUERIES/q$query_file.sql"; } 2> "$RESULTSPATH/$filename.txt"
        if  [ $COLLECTL = "true" ]; then 
            kill $COLLECTL_PID
        fi
       
        mv "$MONETDBQUERIES/q$query_file.sql.bak" "$MONETDBQUERIES/q$query_file.sql"
            ;;
        *)
            echo "Unsupported system: $SYSTEM"
            exit 1
            ;;
    esac
done
    collectl -p $RESULTSPATH/collectl/$filename*.gz -scdnm -P  > $RESULTSPATH/collectl/$filename.csv
    if [[ $query_file == '20' ]]; then
        case "$SYSTEM" in
            duckdb)

                "$PYTHONEXEC" "$DUCKPATH" --duckdb-dbfile "$DUCKDBPATH/$DATAB".db  --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/$DATAB" --duckdb-sql "$DUCKDBQUERIES/q$query_file.sql" &>/dev/null
                # "$PYTHONEXEC" "$DUCKPATH" --duckdb-dbfile "$DUCKDBPATH/$DATAB".db  --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/$DATAB" --duckdb-sql "$DUCKDBQUERIES/q1.sql" &>/dev/null
                ;;
            sqlite3)
                "$PYTHONEXEC" "$SQLITEPATH"  "$SQLITEDBPATH/$DATAB".db "$SQLITEQUERIES/q$query_file.sql" "$SQLITESCALAR/scalar" "$SQLITEAGGRS/aggrs" &>/dev/null
                # "$PYTHONEXEC" "$SQLITEPATH"  "$SQLITEDBPATH/$DATAB".db "$SQLITEQUERIES/q1.sql" "$SQLITESCALAR/scalar" "$SQLITEAGGRS/aggrs" &>/dev/null
                ;;
            sqlitevtab)
                :
                ;;
            postgres)
                $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$POSTGRESQUERIES/q$query_file.sql" &>/dev/null

                $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB"  -f "$POSTGRESQUERIES/create_index.sql"        
         
                ;;
            monetdb)
                
                $MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance < "$MONETDBQUERIES/q$query_file.sql" &>/dev/null

                ;;
            *)
                echo "Unsupported system: $SYSTEM"
                exit 1
                ;;
        esac
    elif [[ $query_file == '21' ]]; then
        QUERY21_REVERT="$RESULTSPATH/script/$filename"-revert.sql
        cat <<EOF > "$QUERY21_REVERT"
delete from projects_artifacts where provenance='crossref';
EOF
        case "$SYSTEM" in
            duckdb)

                "$PYTHONEXEC" "$DUCKPATH" --duckdb-dbfile "$DUCKDBPATH/$DATAB".db  --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/$DATAB" --duckdb-sql "$QUERY21_REVERT"  &>/dev/null
                ;;
            sqlite3)
                :
                ;;
            sqlitevtab)
                "$PYTHONEXEC" "$SQLITEVTABPATH" -d "$SQLITEDBPATH/$DATAB".db -f "$QUERY21_REVERT" &>/dev/null
                ;;
            postgres)
    
                $PSQLPATH -U $PSQLUSER -p $PSQLPORT "$DATAB" -f "$QUERY21_REVERT" &>/dev/null

                ;;
            monetdb)
                $MONETDBPATH -p $MONETDBPORT -d "$DATAB" -f trash -H -t performance < "$QUERY21_REVERT" &>/dev/null
                ;;
            *)
                echo "Unsupported system: $SYSTEM"
                exit 1
                ;;
        esac

    fi
   
done
fi
if [ "$SYSTEM" = "monetdb" ]  &&  [ $NTHREADS -gt  0 ];then
            # echo $NTHREADS
            $MONETDBBINPATH/monetdb -p $MONETDBPORT  stop "$DATAB"
            $MONETDBBINPATH/monetdb -p $MONETDBPORT  set nthreads=$DEFAULT_THREADS "$DATAB"
            $MONETDBBINPATH/monetdb -p $MONETDBPORT  start "$DATAB"
fi
rm -rf "$RESULTSPATH/script/"*
