#!/bin/bash

input_file="$1"
shift

execution_time=$(grep -oP 'run:\K[0-9]+\.[0-9]+' "$input_file")
cpu_time=$(grep -oP 'clk:\K[0-9]+\.[0-9]+' "$input_file")
echo "Execution Time: $execution_time ms"  > "$input_file"
echo "Process Time: $cpu_time ms" >> "$input_file"

