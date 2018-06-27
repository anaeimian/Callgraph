import time
from datetime import date
import math
import statistics
import numpy as np
import matplotlib.pyplot as plt


def add_remove_diff(dates_array, changes):
    adds_removes1 = []
    removes_adds1 = []
    if changes[0] == "add":
        if len(dates_array) > 1:
            for index in range(math.ceil(float(len(dates_array)) / 2) - 1):
                removes_adds1.append(date_diff_days(dates_array[(2 * index) + 1], dates_array[(2 * index) + 2]))
            for index in range(math.floor(float(len(dates_array)) / 2)):
                adds_removes1.append(date_diff_days(dates_array[2 * index], dates_array[2 * index + 1]))
    return adds_removes1, removes_adds1


def date_diff_days(date1, date2):
    date1 = int(date1)
    date2 = int(date2)
    if date1 < date2:
        year1 = time.gmtime(date1).tm_year
        month1 = time.gmtime(date1).tm_mon
        day1 = time.gmtime(date1).tm_mday
        year2 = time.gmtime(date2).tm_year
        month2 = time.gmtime(date2).tm_mon
        day2 = time.gmtime(date2).tm_mday
        days = (date(year2, month2, day2) - date(year1, month1, day1)).days
        return days
    return 0


def reformat_dates(date_array):
    array = []
    for item in date_array:
        item = int(item)
        year = time.gmtime(item).tm_year
        month = time.gmtime(item).tm_mon
        day = time.gmtime(item).tm_mday
        array.append(str(year) + "-" + str(month) + "-" + str(day))
    return array


with open('edge_life_cycle_map.txt') as edge_life_cycle_map_file:
    edge_life_cycle_map = eval(edge_life_cycle_map_file.read())

removes_adds_array = []
adds_removes_array = []
index = 0
add_remove_add_array = []
vertex_changes_map_add_remove = {}
vertex_changes_map_add_remove_callers = {}
vertex_changes_map_add_remove_length = {}

vertex_changes_map_remove_add = {}
vertex_changes_map_remove_add_callers = {}
vertex_changes_map_remove_add_length = {}
remove_add_remove_array = []
for key, value in edge_life_cycle_map.items():
    adds_removes, removes_adds = add_remove_diff(value['dates'], value['changes'])
    for item in adds_removes:
        if item < 2:
            try:
                vertex = vertex_changes_map_add_remove[key[1]]
            except:
                vertex = 0
            vertex += 1
            vertex_changes_map_add_remove[key[1]] = vertex

            try:
                callers = vertex_changes_map_add_remove_callers[key[1]]
            except:
                callers = []
            callers.append(key[0])
            vertex_changes_map_add_remove_callers[key[1]] = callers

    for item in removes_adds:
        if item < 2:
            try:
                vertex = vertex_changes_map_remove_add[key[1]]
            except:
                vertex = 0
            vertex += 1
            vertex_changes_map_remove_add[key[1]] = vertex

            try:
                callers = vertex_changes_map_remove_add_callers[key[1]]
            except:
                callers = []
            callers.append(key[0])
            vertex_changes_map_remove_add_callers[key[1]] = callers


for key, value in vertex_changes_map_add_remove_callers.items():
    vertex_changes_map_add_remove_callers[key] = list(set(value))
    vertex_changes_map_add_remove_length[key] = len(list(set(value)))

for key, value in vertex_changes_map_remove_add_callers.items():
    vertex_changes_map_remove_add_callers[key] = list(set(value))
    vertex_changes_map_remove_add_length[key] = len(list(set(value)))

for key, value in vertex_changes_map_add_remove_length.items():
    adds_removes_array.append(value)

for key, value in vertex_changes_map_remove_add_length.items():
    removes_adds_array.append(value)

print(vertex_changes_map_add_remove)
print(vertex_changes_map_remove_add)
print()
print(vertex_changes_map_add_remove_callers)
# print(vertex_changes_map_add_remove_length)
print()
print(vertex_changes_map_remove_add_callers)
# print(vertex_changes_map_remove_add_length)
print()

# print(sorted(vertex_changes_map_add_remove_length,key = vertex_changes_map_add_remove_length.get))
print(sorted(adds_removes_array))
# print(sorted(vertex_changes_map_remove_add_length,key = vertex_changes_map_remove_add_length.get))
print(sorted(removes_adds_array))
