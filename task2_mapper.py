#!/usr/bin/env python3

import sys
import math


def read_initialization():
    with open("initialization.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    max_iterations = int(lines[0])

    medoids = []
    for line in lines[1:]:
        x, y = line.split()
        medoids.append((float(x), float(y)))

    return max_iterations, medoids


def distance(point, medoid):
    dx = point[0] - medoid[0]
    dy = point[1] - medoid[1]
    return math.sqrt(dx * dx + dy * dy)


max_iterations, medoids = read_initialization()

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

    for index in range(1, len(medoids)):
        current_distance = distance(point, medoids[index])

        if current_distance < closest_distance:
            closest = index
            closest_distance = current_distance

    print(
        f"{closest}\t"
        f"{dropoff_x:.3f},{dropoff_y:.3f},{closest_distance:.3f}"
    )
