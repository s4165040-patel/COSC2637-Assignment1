#!/bin/bash

INPUT="/Input/Trips.txt"
OUTPUT="/Output/task2"

INIT_FILE="initialization.txt"
MEDOIDS_FILE="task2_medoids.txt"

STREAMING_JAR="/usr/lib/hadoop/hadoop-streaming.jar"

echo "Task 2 - PAM Clustering"

# Check initialization file
if [ ! -f "$INIT_FILE" ]; then
    echo "ERROR: $INIT_FILE not found."
    exit 1
fi

# First line = maximum number of iterations
MAX_ITER=$(head -n 1 "$INIT_FILE")

# Remaining lines = initial medoids
tail -n +2 "$INIT_FILE" > "$MEDOIDS_FILE"

echo "Maximum iterations: $MAX_ITER"
echo "Initial medoids:"
cat "$MEDOIDS_FILE"

# Removing old final output
if hdfs dfs -test -e "$OUTPUT"; then
    hdfs dfs -rm -r "$OUTPUT"
fi

# Removing old intermediate output
for i in $(seq 1 "$MAX_ITER"); do
    hdfs dfs -rm -r "/tmp/task2_iter_$i" 2>/dev/null
done

LAST_ITER=0

for ((ITER=1; ITER<=MAX_ITER; ITER++))
do
    LAST_ITER=$ITER

    echo ""
    echo "Iteration $ITER"
    

    ITER_OUTPUT="/tmp/task2_iter_$ITER"

    echo "Current medoids:"
    cat "$MEDOIDS_FILE"

   
    hadoop jar "$STREAMING_JAR" \
        -D mapreduce.job.reduces=3 \
        -input "$INPUT" \
        -output "$ITER_OUTPUT" \
        -mapper "python3 task2_mapper.py $MEDOIDS_FILE" \
        -reducer "python3 task2_reducer.py" \
        -file task2_mapper.py \
        -file task2_reducer.py \
        -file "$MEDOIDS_FILE"
   
    if [ $? -ne 0 ]; then
        echo "ERROR: Hadoop job failed at iteration $ITER."
        exit 1
    fi

    echo ""
    echo "Iteration $ITER result:"
    hdfs dfs -cat "$ITER_OUTPUT"/part-* | sort -n

    # Extracting new medoid coordinates
    hdfs dfs -cat "$ITER_OUTPUT"/part-* | \
        sort -n | \
        awk -F '\t' '{print $2 " " $3}' > "$MEDOIDS_FILE.new"

    # Checking number of medoids
    MEDOID_COUNT=$(wc -l < "$MEDOIDS_FILE.new")

    if [ "$MEDOID_COUNT" -eq 0 ]; then
        echo "ERROR: No medoids were produced."
        exit 1
    fi

    # Comparing old and new medoids
    if cmp -s "$MEDOIDS_FILE" "$MEDOIDS_FILE.new"; then
        echo ""
        echo "Medoids have converged."
        break
    fi

    mv "$MEDOIDS_FILE.new" "$MEDOIDS_FILE"
done

echo ""
echo "Creating final output"


# Removing existing final output
if hdfs dfs -test -e "$OUTPUT"; then
    hdfs dfs -rm -r "$OUTPUT"
fi

# Final output must contain exactly:
# medoid_x medoid_y #points avg_dissimilarity

hdfs dfs -mkdir -p "$OUTPUT"

hdfs dfs -cat "/tmp/task2_iter_$LAST_ITER"/part-* | \
    sort -n | \
    awk -F '\t' 'BEGIN{OFS="\t"} {print $2, $3, $4, $5}' | \
    hdfs dfs -put - "$OUTPUT/part-00000"

echo ""
echo "FINAL TASK 2 OUTPUT"

hdfs dfs -cat "$OUTPUT/part-00000"

echo ""
echo "Task 2 complete."

# Cleaning intermediate HDFS output
for i in $(seq 1 "$MAX_ITER"); do
    hdfs dfs -rm -r "/tmp/task2_iter_$i" 2>/dev/null
done

rm -f "$MEDOIDS_FILE" "$MEDOIDS_FILE.new"
