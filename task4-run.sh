#!/bin/bash

# Remove the HDFS output directory forcefully and recursively.
hadoop fs -rm -r -f /Output/task4

hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
-D stream.num.map.output.key.fields=2 \
-D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
-D mapred.text.key.partitioner.options=-k1,1 \
-D mapred.text.key.comparator.options='-k1,1 -k2,2n' \
-D mapreduce.job.reduces=3 \
-file ./task4-mapper.py \
-mapper "python3 task4-mapper.py" \
-file ./task4-reducer.py \
-reducer "python3 task4-reducer.py" \
-input /Input/Trips.txt \
-output /Output/task4 \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner