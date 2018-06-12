import time
from datetime import date
import math
def add_remove_diff(dates_array, changes):
    adds = []
    removes = []
    if changes[0] == "add":
        if len(dates_array) > 2:
            for index in range(len(dates_array)-2):
                adds.append(date_diff_days(dates_array[index] , dates_array[index+2]))

            if len(dates_array)>3:
                for index in range(math.floor(float(len(dates_array))/2) - 1):
                    removes.append(date_diff_days(dates_array[index+1] , dates_array[index+3]))

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
        return (date(year2, month2, day2) - date(year1, month1, day1)).days

with open('edge_life_cycle_map.txt') as edge_life_cycle_map_file:
    edge_life_cycle_map = eval(edge_life_cycle_map_file.read())
