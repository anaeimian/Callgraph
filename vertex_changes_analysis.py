import time
from datetime import date
import math
import statistics
import numpy as np
import matplotlib.pyplot as plt
import csv


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


def write_map_to_excel(map_var, file_name):
    csv_file = open(file_name, 'w')
    for key2, value2 in map_var.items():
        csv_file.write(str(key2) + ', ' + str(value2) + '\n')
    csv_file.close()


with open('edge_life_cycle_map.txt') as edge_life_cycle_map_file:
    edge_life_cycle_map = eval(edge_life_cycle_map_file.read())

removes_adds_array = []
adds_removes_array = []
index = 0
add_remove_add_array = []
vertex_changes_map_add_remove_01 = {}
vertex_changes_map_add_remove_total = {}
vertex_changes_map_add_remove_callers_01 = {}
vertex_changes_map_add_remove_callers_total = {}
vertex_changes_map_add_remove_length_01 = {}
vertex_changes_map_add_remove_length_total = {}

vertex_changes_map_remove_add_01 = {}
vertex_changes_map_remove_add_total = {}
vertex_changes_map_remove_add_callers_01 = {}
vertex_changes_map_remove_add_callers_total = {}
vertex_changes_map_remove_add_length_01 = {}
vertex_changes_map_remove_add_length_total = {}

vertex_changes_map_add_remove_sum_01 = {}
vertex_changes_map_remove_add_sum_01 = {}
vertex_changes_map_add_remove_sum_total = {}
vertex_changes_map_remove_add_sum_total = {}

remove_add_remove_array = []
for key, value in edge_life_cycle_map.items():
    adds_removes, removes_adds = add_remove_diff(value['dates'], value['changes'])
    for item in adds_removes:
        if item < 2:
            try:
                vertex = vertex_changes_map_add_remove_01[key[1]]
            except:
                vertex = 0
            vertex += 1
            vertex_changes_map_add_remove_01[key[1]] = vertex

            try:
                callers = vertex_changes_map_add_remove_callers_01[key[1]]
            except:
                callers = []
            callers.append(key[0])
            vertex_changes_map_add_remove_callers_01[key[1]] = callers
        else:
            try:
                vertex = vertex_changes_map_add_remove_01[key[1]]
            except:
                vertex = 0
            vertex_changes_map_add_remove_01[key[1]] = vertex

            try:
                callers = vertex_changes_map_add_remove_callers_01[key[1]]
            except:
                callers = []
            vertex_changes_map_add_remove_callers_01[key[1]] = callers




        try:
            vertex = vertex_changes_map_add_remove_total[key[1]]
        except:
            vertex = 0
        vertex += 1
        vertex_changes_map_add_remove_total[key[1]] = vertex

        try:
            callers = vertex_changes_map_add_remove_callers_total[key[1]]
        except:
            callers = []
        callers.append(key[0])
        vertex_changes_map_add_remove_callers_total[key[1]] = callers
    for item in removes_adds:
        if item < 2:
            try:
                vertex = vertex_changes_map_remove_add_01[key[1]]
            except:
                vertex = 0
            vertex += 1
            vertex_changes_map_remove_add_01[key[1]] = vertex

            try:
                callers = vertex_changes_map_remove_add_callers_01[key[1]]
            except:
                callers = []
            callers.append(key[0])
            vertex_changes_map_remove_add_callers_01[key[1]] = callers
        else:
            try:
                vertex = vertex_changes_map_remove_add_01[key[1]]
            except:
                vertex = 0
            vertex_changes_map_remove_add_01[key[1]] = vertex

            try:
                callers = vertex_changes_map_remove_add_callers_01[key[1]]
            except:
                callers = []
            vertex_changes_map_remove_add_callers_01[key[1]] = callers




        try:
            vertex = vertex_changes_map_remove_add_total[key[1]]
        except:
            vertex = 0
        vertex += 1
        vertex_changes_map_remove_add_total[key[1]] = vertex

        try:
            callers = vertex_changes_map_remove_add_callers_total[key[1]]
        except:
            callers = []
        callers.append(key[0])
        vertex_changes_map_remove_add_callers_total[key[1]] = callers

for key, value in vertex_changes_map_add_remove_callers_01.items():
    vertex_changes_map_add_remove_callers_01[key] = list(set(value))
    vertex_changes_map_add_remove_length_01[key] = len(list(set(value)))

for key, value in vertex_changes_map_remove_add_callers_01.items():
    vertex_changes_map_remove_add_callers_01[key] = list(set(value))
    vertex_changes_map_remove_add_length_01[key] = len(list(set(value)))

for key, value in vertex_changes_map_add_remove_01.items():
    vertex_changes_map_add_remove_sum_01[key] = value + vertex_changes_map_add_remove_length_01[key]

for key, value in vertex_changes_map_remove_add_01.items():
    vertex_changes_map_remove_add_sum_01[key] = value + vertex_changes_map_remove_add_length_01[key]

for key, value in vertex_changes_map_add_remove_callers_total.items():
    vertex_changes_map_add_remove_callers_total[key] = list(set(value))
    vertex_changes_map_add_remove_length_total[key] = len(list(set(value)))

for key, value in vertex_changes_map_remove_add_callers_total.items():
    vertex_changes_map_remove_add_callers_total[key] = list(set(value))
    vertex_changes_map_remove_add_length_total[key] = len(list(set(value)))

for key, value in vertex_changes_map_add_remove_total.items():
    vertex_changes_map_add_remove_sum_total[key] = value + vertex_changes_map_add_remove_length_total[key]

for key, value in vertex_changes_map_remove_add_total.items():
    vertex_changes_map_remove_add_sum_total[key] = value + vertex_changes_map_remove_add_length_total[key]

# for key, value in vertex_changes_map_add_remove_length.items():
#     adds_removes_array.append(value)
#
# for key, value in vertex_changes_map_remove_add_length.items():
#     removes_adds_array.append(value)
write_map_to_excel(vertex_changes_map_add_remove_sum_01, 'vertex_changes_map_add_remove_sum_01.csv')
write_map_to_excel(vertex_changes_map_add_remove_01, 'vertex_changes_map_add_remove_01.csv')
write_map_to_excel(vertex_changes_map_add_remove_length_01, 'vertex_changes_map_add_remove_length_01.csv')
write_map_to_excel(vertex_changes_map_remove_add_sum_01, 'vertex_changes_map_remove_add_sum_01.csv')
write_map_to_excel(vertex_changes_map_remove_add_01, 'vertex_changes_map_remove_add_01.csv')
write_map_to_excel(vertex_changes_map_remove_add_length_01, 'vertex_changes_map_remove_add_length_01.csv')


write_map_to_excel(vertex_changes_map_add_remove_sum_total, 'vertex_changes_map_add_remove_sum_total.csv')
write_map_to_excel(vertex_changes_map_add_remove_total, 'vertex_changes_map_add_remove_total.csv')
write_map_to_excel(vertex_changes_map_add_remove_length_total, 'vertex_changes_map_add_remove_length_total.csv')
write_map_to_excel(vertex_changes_map_remove_add_sum_total, 'vertex_changes_map_remove_add_sum_total.csv')
write_map_to_excel(vertex_changes_map_remove_add_total, 'vertex_changes_map_remove_add_total.csv')
write_map_to_excel(vertex_changes_map_remove_add_length_total, 'vertex_changes_map_remove_add_length_total.csv')

# print(vertex_changes_map_add_remove)
# print(vertex_changes_map_add_remove_length)
# print(vertex_changes_map_add_remove_sum)
# print()
# print(vertex_changes_map_remove_add)
# print(vertex_changes_map_remove_add_length)
# print(vertex_changes_map_remove_add_sum)

# print(vertex_changes_map_add_remove_callers)
# # print(vertex_changes_map_add_remove_length)
# print()
# print(vertex_changes_map_remove_add_callers)
# # print(vertex_changes_map_remove_add_length)
# print()

# print(sorted(vertex_changes_map_add_remove_length,key = vertex_changes_map_add_remove_length.get))
print(sorted(adds_removes_array))
# print(sorted(vertex_changes_map_remove_add_length,key = vertex_changes_map_remove_add_length.get))
print(sorted(removes_adds_array))
