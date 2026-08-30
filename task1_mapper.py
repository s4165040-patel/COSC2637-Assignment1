#!/usr/bin/env python3

import sys

# Store totals for each taxi and distance category while this mapper runs.
taxi_totals = {}

for record in sys.stdin:
    record = record.strip()

    if not record:
        continue

    columns = record.split(",")

    if len(columns) != 8:
        continue

    try:
        taxi_id = columns[1].strip()
        fare = float(columns[2])
        distance = float(columns[3])
    except ValueError:
        continue

    # Divide trips into the three distance groups from the assignment.
    if distance < 100:
        category = "short"
    elif distance < 200:
        category = "medium"
    else:
        category = "long"

    group = (taxi_id, category)

    if group not in taxi_totals:
        taxi_totals[group] = [0, 0.0, fare, fare]

    taxi_totals[group][0] += 1
    taxi_totals[group][1] += fare

    if fare > taxi_totals[group][2]:
        taxi_totals[group][2] = fare

    if fare < taxi_totals[group][3]:
        taxi_totals[group][3] = fare


# Send one combined record for each taxi/category to the reducer.
for (taxi_id, category), totals in taxi_totals.items():
    count, total_fare, highest_fare, lowest_fare = totals

    print(
        f"{taxi_id}\t{category}\t"
        f"{count}\t{total_fare:.2f}\t"
        f"{highest_fare:.2f}\t{lowest_fare:.2f}"
    )
