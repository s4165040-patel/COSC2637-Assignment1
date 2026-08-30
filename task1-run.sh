#!/bin/bash

INPUT="/Input/Trips.txt"
OUTPUT="/Output/task1"
STREAMING_JAR="/usr/lib/hadoop/hadoop-streaming.jar"

echo "Starting Task 1..."

if hdfs dfs -test -e "$OUTPUT"; then
    echo "Removing existing output directory..."
    hdfs dfs -rm -r "$OUTPUT"
fi

echo "Running Hadoop Streaming job..."

hadoop jar "$STREAMING_JAR" \
    -D mapreduce.job.reduces=3 \
    -input "$INPUT" \
    -output "$OUTPUT" \
    -mapper "python3 task1_mapper.py" \
    -reducer "python3 task1_reducer.py" \
    -file task1_mapper.py \
    -file task1_reducer.py

echo "Task 1 finished."

if hdfs dfs -test -e "$OUTPUT"; then
    echo "Output:"
    hdfs dfs -cat "$OUTPUT/part-*"
else
    echo "Task 1 failed: output directory was not created."
    exit 1
fi
