#!/usr/bin/env python3

import sys

current_cluster = None
points = 0
distance_total = 0.0

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    fields = line.split("\t")

    if len(fields) != 2:
        continue

    cluster_id = fields[0]

    try:
        values = fields[1].split(",")

        if len(values) != 3:
            continue

        x = float(values[0])
        y = float(values[1])
        dissimilarity = float(values[2])

    except ValueError:
        continue

    if current_cluster is not None and cluster_id != current_cluster:
        average = distance_total / points if points else 0.0

   )
