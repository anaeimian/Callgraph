import time
from datetime import date
import math
import statistics
import numpy as np


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
remove_add_remove_array = []
for key, value in edge_life_cycle_map.items():
    adds_removes, removes_adds = add_remove_diff(value['dates'], value['changes'])
    adds_removes_array += adds_removes
    removes_adds_array += removes_adds
    # if 0 in adds_removes or 0 in removes_adds or 1 in adds_removes or 1 in removes_adds or 2 in adds_removes or 2 in removes_adds:
    # if 0 in adds_removes or 0 in removes_adds:
    #     print(key, adds_removes, removes_adds, reformat_dates(value['dates']), value['commits'])
    for number in range(len(removes_adds)):
        if adds_removes[number] == 0 and removes_adds[number] == 0:
            print('add-remove-add - ', key, adds_removes, removes_adds, reformat_dates(value['dates']),
                  value['commits'])
            add_remove_add_array.append(key)
    for number in range(len(adds_removes)-1):
        if removes_adds[number] == 0 and adds_removes[number + 1] == 0:
            print('remove-add-remove - ', key, adds_removes, removes_adds, reformat_dates(value['dates']),
                  value['commits'])
            remove_add_remove_array.append(key)
    # print('dates: ', reformat_dates(value['dates']))
    # print('adds_removes: ', adds_removes)
    # print('removes_adds: ', removes_adds)
print(len(add_remove_add_array), len(remove_add_remove_array))
print("########################################")

print('average adds-removes array:', statistics.mean(adds_removes_array))
print('average removes-adds array:', statistics.mean(removes_adds_array))

print('mode adds-removes array:', statistics.mode(adds_removes_array))
print('mode removes-adds array:', statistics.mode(removes_adds_array))

print("########################################")

print('0.25 percentile adds-removes array: ', np.percentile(adds_removes_array, 25))
print('0.5 percentile adds-removes array: ', np.percentile(adds_removes_array, 50))
print('0.75 percentile adds-removes array: ', np.percentile(adds_removes_array, 75))
print()
print('0.25 percentile removes-adds array: ', np.percentile(removes_adds_array, 25))
print('0.5 percentile removes-adds array: ', np.percentile(removes_adds_array, 50))
print('0.75 percentile removes-adds array: ', np.percentile(removes_adds_array, 75))

print("########################################")

print('adds-removes array:', sorted(adds_removes_array), len(adds_removes_array))
print('adds-removes array length:', len(adds_removes_array))
print('removes-adds array:', sorted(removes_adds_array), len(removes_adds_array))
print('removes-adds array length:', len(removes_adds_array))
