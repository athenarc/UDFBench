#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <resultscsvpath>"
    exit 1
fi
resultscsvpath="$1"
shift

engines=( $(find "$PWD"/engines/ -mindepth 1 -maxdepth 1 -type d | xargs -n 1 basename ) )
echo "dbname, experiment_name, exec_time, cpu_time, collectl_file_path" > "$resultscsvpath"

for system in "${engines[@]}"; do
    # echo "System $system"
    if [ -f "$PWD"/engines/"$system"/scripts/"$system"_config.sh ]; then
        source "$PWD"/engines/"$system"/scripts/"$system"_config.sh
        SYSTEM="${system^^}"
        result_var="${SYSTEM}RESULTSPATH"
        curresultpath="${!result_var}"
        if [ -d "$curresultpath"/experiments ]; then
            for file in "$curresultpath"/experiments/*.txt; do
                experiment_name=$(basename "$file" .txt)
                execution_time=$(grep -oP 'Execution Time: \K[0-9]+\.[0-9]+' "$file")
                cpu_time=$(grep -oP 'Process Time: \K[0-9]+\.[0-9]+' "$file")
                if  [ -d "$curresultpath"/collectl ]; then
                    collectl_file_path="$curresultpath"/collectl/"$experiment_name".csv
                    if [ ! -f "$collectl_file_path" ]; then
                        collectl_file_path=""
                    fi
                else
                    collectl_file_path=""
                fi
    
                if [ -z "$execution_time" ]; then
                    execution_time=""
                fi
                if [ -z "$cpu_time" ]; then
                    cpu_time=""
                fi
                echo  "$system, $experiment_name, $execution_time, $cpu_time, $collectl_file_path" >> "$resultscsvpath"
            done
        fi
    fi
done
