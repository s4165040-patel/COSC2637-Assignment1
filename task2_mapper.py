#!/usr/bin/env python3

import sys
import math


def read_medoids(filename):
    medoids = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) != 2:
                continue

            medoids.append((float(parts[0]), float(parts[1])))

    return medoids


def distance(point, medoid):
    dx = point[0] - medoid[0]
    dy = point[1] - medoid[1]
    return math.sqrt(dx * dx + dy * dy)


if len(sys.argv) != 2:
    sys.stderr.write("Usage: task2_mapper.py medoids_file\n")
    sys.exit(1)

medoids = read_medoids(sys.argv[1])

if not medoids:
    sys.stderr.write("ERROR: No medoids found\n")
    sys.exit(1)


for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    fields = line.split(",")

    if len(fields) != 8:
        continue

    try:
        dropoff_x = float(fields[6])
        dropoff_y = float(fields[7])
    except ValueError:
        continue

    point = (dropoff_x, dropoff_y)

    closest = 0
    closest_distance = distance(point, medoids[0])

    for i in range(1, len(medoids)):
        current_distance = distance(point, medoids[i])

        if current_distance < closest_distance:
            closest = i
            closest_distance = current_distance

    print(
        f"{closest}\t"
        f"{dropoff_x:.3f},{dropoff_y:.3f},{closest_distance:.3f}"
    )
