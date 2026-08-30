#!/usr/bin/env python3
import sys
# Task 4: mean and standard deviation of trip distance per taxi
# Trips.txt: Trip ID, Taxi ID, fare, distance, pickup_x, pickup_y, dropoff_x, dropoff_y
# input comes from standard input STDIN
partials = {}

for line in sys.stdin:
    line = line.strip() #remove leading and trailing whitespaces
    fields = line.split(",") #split the line into fields and returns as a list

    if len(fields) != 8:
        continue

    try:
        taxi = fields[1].strip()
        distance = float(fields[3])
    except ValueError:
        continue

    print('%s\t%s\t%s' % (taxi,"1",fields[3])) #Emit <key, value> pairs

    if taxi not in partials:
        partials[taxi] = [0, 0.0]

    partials[taxi][0] += 1
    partials[taxi][1] += distance

# Send one combined record for each taxi to the reducer.
for taxi in partials:
    count, total = partials[taxi]
    print('%s\t%s\t%d,%s' % (taxi,"0",count,repr(total))) #Emit <key, value> pairs