#!/bin/bash

source $PWD'/utilities/config.sh'


DISK="$1"
shift

RUNEXP="$1"
shift

DEPLOY="$1"
shift

DOWNLOAD="$1"
shift

SETUP="$1"
shift

    if [ $RUNEXP = 'yes' ] || [ $DEPLOY = 'yes' ]; then
        read -r -p "To run the experiment or deploy a database, please enter the sizes separated by spaces  (use 't' for tiny, 's' for small, 'm' for medium, 'l' for large): " -a arr 
    fi

    case $DOWNLOAD in
        yes)
            $PWD'/dataset/raw_data/download_dateset.sh'

            ;;
        no)
            :
            ;;
        *)
            :
            ;;
    esac

    case $SETUP in
        yes)
            export CURRENT=$PWD
            mkdir -p $PWD'/downloads'
            for system in "$@"; do
                $PWD'/utilities/'$system'_setup.sh'
                for database in t; do
                    $PWD'/utilities/createdatabases.sh' $system $database $DISK
                done
            done           
            ;;
        no)
            :
            ;;
        *)
            :
            ;;
    esac


    case $DEPLOY in
        yes)
            if [[ $SETUP == "no" ]]; then
                for system in "$@";do
                    for database in "${arr[@]}"; do
                        $PWD'/utilities/createdatabases.sh' $system $database $DISK
                        $PWD'/utilities/deploybenchmark.sh' $system $database $DISK
                    done
                done
            else
                for system in "$@";do
                    for database in "${arr[@]}"; do
                        $PWD'/utilities/deploybenchmark.sh' $system $database $DISK
                    done
                done            
            fi
            ;;
        no)
            :
            ;;
        *)
            :
            ;;
    esac


    
    case $RUNEXP in
        yes)
            for database in "${arr[@]}"; do
                for system in "$@"; do
                    # echo "$database $system"

                    if [[ $system == "postgres" ]] ; then
                        $PWD'/utilities/runexperiment.sh' $system $database t0 cold $DISK false true \
                        1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
                    elif [[ $system == "monetdb" ]] ; then
                        $PWD'/utilities/runexperiment.sh' $system $database t0 cold $DISK false true\
                        1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
                    elif [[ $system == "duckdb" ]]; then
                        $PWD'/utilities/runexperiment.sh' $system $database  t0 cold $DISK false true\
                        1 2 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21  
                    elif [[ $system == "sqlite3" ]]; then
                        $PWD'/utilities/runexperiment.sh' $system $database  t0 cold $DISK false true\
                        1 4 8 12 14 20
                        $PWD'/utilities/runexperiment.sh' sqlitevtab $database t0 cold $DISK false true \
                        2 5 6 7 9 10 11 13 15 16 17 18 19 21
                    fi
                done
            done
            ;;
        no)
            :
            ;;
        *)
            :
            ;;
    esac

