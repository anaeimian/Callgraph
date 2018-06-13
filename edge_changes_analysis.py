import time
from datetime import date
import math
import statistics


def add_remove_diff(dates_array, changes):
    adds_removes = []
    adds_removes2 = []
    adds = []
    removes = []
    if changes[0] == "add":
        if len(dates_array) > 1:
            for index in range(len(dates_array) - 1):
                adds_removes.append(date_diff_days(dates_array[index], dates_array[index + 1]))
            for index in range(math.floor(float(len(dates_array)) / 2)):
                adds_removes2.append(date_diff_days(dates_array[2 * index], dates_array[2 * index + 1]))
            if len(dates_array) > 2:
                for index in range(math.ceil(float(len(dates_array)) / 2) - 1):
                    adds.append(date_diff_days(dates_array[2 * index], dates_array[2 * index + 2]))

                if len(dates_array) > 3:
                    for index in range(math.floor(float(len(dates_array)) / 2) - 1):
                        removes.append(date_diff_days(dates_array[2*index + 1], dates_array[2*index + 3]))
    return adds, removes, adds_removes, adds_removes2


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
    return ""


with open('edge_life_cycle_map.txt') as edge_life_cycle_map_file:
    edge_life_cycle_map = eval(edge_life_cycle_map_file.read())

adds_array = []
removes_array = []
adds_removes_array = []
adds_removes_array2 = []
for key, value in edge_life_cycle_map.items():
    adds, removes, adds_removes, adds_removes2 = add_remove_diff(value['dates'], value['changes'])
    adds_array += adds
    removes_array += removes
    adds_removes_array += adds_removes
    adds_removes_array2 += adds_removes2
    print('dates: ', value['dates'])
    print('adds: ', adds)
    print('removes: ', removes)
    print('adds_removes: ', adds_removes)
    print('adds_removes: ', adds_removes)

print("########################################")

print('average adds array:', statistics.mean(adds_array))
print('average removes array:', statistics.mean(removes_array))
print('average adds-removes array:', statistics.mean(adds_removes_array))
print('average adds-removes2 array:', statistics.mean(adds_removes_array2))

print("########################################")

print('adds array:', sorted(adds_array))
print('removes array:', sorted(removes_array))
print('adds-removes array:', sorted(adds_removes_array))
print('adds-removes2 array:', sorted(adds_removes_array2))
