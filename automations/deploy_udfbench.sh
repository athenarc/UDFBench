#!/bin/bash

source $PWD'/automations/config_udfbench.sh'


DISK="$1"

DATASETSPATH=$DATASETSPATHSSD
if [ $DISK = "ssd" ]; then
    true
elif [ $DISK = "hdd" ]; then
    DATASETSPATH=$DATASETSPATHHDD
elif [ $DISK = "mem" ]; then
    DATASETSPATH=$DATASETSPATHMEM
fi

shift

DEPLOY="$1"
shift

DOWNLOAD="$1"
shift

SETUP="$1"
shift

    if [ $DEPLOY = 'yes' ]; then
        read -r -p "To deploy a database, please enter the sizes separated by spaces  (use 't' for tiny, 's' for small, 'm' for medium, 'l' for large): " -a arr 
    fi

    case $DOWNLOAD in
        yes)
            "$DATASETSPATH"/etl/download_dataset.sh
            databases=("small" "medium" "large")
            for database in "${databases[@]}"; do
                mv "$DATASETSPATH"/externalfiles/"$database"/ "$DATASETSPATH"/files/
                "$DATASETSPATH"/csv_to_parquet.sh  "$DATASETSPATH"/csvs "$DATASETSPATH"/parquet $database $PYTHONEXEC
            done
            rm -r "$DATASETSPATH"/externalfiles
            ;;
        no)
            :
            ;;
        *)
            echo "Invalid input"
            ;;
    esac

    engines=( $(find "$PWD"/engines/ -mindepth 1 -maxdepth 1 -type d | xargs -n 1 basename) )

    case $SETUP in
        yes)
            mkdir -p $PWD'/downloads'
            for system in "$@"; do
                if [[ " ${engines[@]} " =~ " $system " ]]; then
                    source "$PWD"/engines/"$system"/scripts/"$system"_config.sh
                    "$PWD"/engines/"$system"/scripts/"$system"_setup.sh $PYTHONEXEC
                else
                    echo "Invalid system"
                fi  
            done           
            ;;
        no)
            :
            ;;
        *)
            echo "Invalid input"
            ;;
    esac


    case $DEPLOY in
        yes)
            for system in "$@";do
                if [[ " ${engines[@]} " =~ " $system " ]]; then
                    source "$PWD"/engines/"$system"/scripts/"$system"_config.sh
                    for database in "${arr[@]}"; do
                        "$PWD"/engines/"$system"/scripts/create_database.sh $database $DISK
                        "$PWD"/engines/"$system"/scripts/create_schema.sh $database $DISK
                        "$PWD"/engines/"$system"/scripts/load_schema.sh $database $DISK $DATASETSPATH $PYTHONEXEC
                    done
                else
                    echo "Invalid system"
                fi
            done
        
            ;;
        no)
            :
            ;;
        *)
            echo "Invalid input"
            ;;
    esac

