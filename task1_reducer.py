#!/usr/bin/env python3

import sys

current_key = None
count = 0
total = 0.0
maximum = 0.0
minimum = 0.0

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    fields = line.split("\t")

    if len(fields) != 6:
        continue

    taxi_id = fields[0]
    trip_type = fields[1]

    try:
        record_count = int(fields[2])
        record_sum = float(fields[3])
        record_max = float(fields[4])
        record_min = float(fields[5])
    except ValueError:
        continue

    key = (taxi_id, trip_type)

    if current_key is not None and key != current_key:
        print(
            f"{current_key[0]}\t{current_key[1]}\t"
            f"{count}\t{total:.2f}\t{maximum:.2f}\t{minimum:.2f}"
        )

        count = 0
        total = 0.0
        maximum = 0.0
        minimum = 0.0

    if current_key is None or key != current_key:
        current_key = key
        maximum = record_max
        minimum = record_min

    count += record_count
    total += record_sum

    if record_max > maximum:
        maximum = record_max

    if record_min < minimum:
        minimum = record_min


if current_key is not None:
    print(
        f"{current_key[0]}\t{current_key[1]}\t"
        f"{count}\t{total:.2f}\t{maximum:.2f}\t{minimum:.2f}"
    )

