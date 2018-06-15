import time
from datetime import date
import math
import statistics


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
for key, value in edge_life_cycle_map.items():
    adds_removes, removes_adds = add_remove_diff(value['dates'], value['changes'])
    adds_removes_array += adds_removes
    removes_adds_array += removes_adds
    if adds_removes or removes_adds:
        print(key, adds_removes, removes_adds, reformat_dates(value['dates']), value['commits'])
    # print('dates: ', reformat_dates(value['dates']))
    # print('adds_removes: ', adds_removes)
    # print('removes_adds: ', removes_adds)

print("########################################")

print('average adds-removes array:', statistics.mean(adds_removes_array))
print('average removes-adds array:', statistics.mean(removes_adds_array))

print("########################################")

print('adds-removes array:', sorted(adds_removes_array))
print('removes-adds array:', sorted(removes_adds_array))