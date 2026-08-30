#!/usr/bin/env python3

import sys
import math


def distance(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return math.sqrt(dx * dx + dy * dy)


def pam_medoid(points):
    if not points:
        return None, 0.0

    best_point = points[0]
    best_cost = float("inf")

    for candidate in points:
        total_distance = 0.0

        for point in points:
            total_distance += distance(candidate, point)

        average_distance = total_distance / len(points)

        if average_distance < best_cost:
            best_cost = average_distance
            best_point = candidate

    return best_point, best_cost


current_cluster = None
points = []


def process_cluster(cluster_id, cluster_points):
    if not cluster_points:
        return

    medoid, avg_distance = pam_medoid(cluster_points)

    print(
        f"{cluster_id}\t"
        f"{medoid[0]:.3f}\t"
        f"{medoid[1]:.3f}\t"
        f"{len(cluster_points)}\t"
        f"{avg_distance:.2f}"
    )


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

    except ValueError:
        continue

    if current_cluster is not None and cluster_id != current_cluster:
        process_cluster(current_cluster, points)
        points = []

    current_cluster = cluster_id
    points.append((x, y))


if current_cluster is not None:
    process_cluster(current_cluster, points)
