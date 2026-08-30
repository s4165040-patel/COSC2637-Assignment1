#!/usr/bin/env python3
import sys
import math
# Task 4: mean and standard deviation of trip distance per taxi
# Input arrives as taxi_id \t tag \t value, sorted so that all "0" records
# (count,sum) for a taxi arrive before its "1" records (the distances).
current_taxi = None
count = 0
total = 0.0
sq_total = 0.0
mean = None

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')

    if len(fields) != 3:
        continue

    taxi = fields[0]
    tag = fields[1]
    value = fields[2]

    if current_taxi is not None and taxi != current_taxi:
        print('%s\t%.2f\t%.2f' % (current_taxi, total/count, math.sqrt(sq_total/count)))
        count = 0
        total = 0.0
        sq_total = 0.0
        mean = None

    current_taxi = taxi

    if tag == "0":
        try:
            partial = value.split(',')
            count += int(partial[0])
            total += float(partial[1])
        except ValueError:
            continue
    else:
        if mean is None:
            mean = total / count
        try:
            distance = float(value)
        except ValueError:
            continue
        sq_total += (distance - mean) * (distance - mean)

if current_taxi is not None:
    print('%s\t%.2f\t%.2f' % (current_taxi, total/count, math.sqrt(sq_total/count)))