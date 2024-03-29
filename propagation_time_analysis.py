# This file determines whether a bug was propagated from a source to a destination (propagation means source had a buggy change prior to destination or the oppsite side)
import time
import json
from datetime import date
import my_statistics


def source_dst_date_diff(source_date_array, dst_date_array):
    for item1 in source_date_array:
        for item2 in dst_date_array:
            item1 = int(item1)
            item2 = int(item2)
            if item1 < item2:
                year1 = time.gmtime(item1).tm_year
                month1 = time.gmtime(item1).tm_mon
                day1 = time.gmtime(item1).tm_mday
                year2 = time.gmtime(item2).tm_year
                month2 = time.gmtime(item2).tm_mon
                day2 = time.gmtime(item2).tm_mday
                return (date(year2, month2, day2) - date(year1, month1, day1)).days
    return 0


def src_dst_exists(src, dst, time_map):
    for key1, value1 in time_map.items():
        for item1 in value1:
            if key1 == src and item1[0] == dst:
                return True
    return False


def insert_time_map(src, dst, propagation_time, time_map):
    try:
        array = time_map[src]
    except Exception as e:
        print(e)
        array = []
    array.append((dst, propagation_time))
    time_map[src] = array


def get_callers(node, call_graph):
    callers = []
    for caller, callees in call_graph.items():
        if node in callees:
            callers.append(caller)
    return callers


def get_callee_number(callsmap):
    counter = 0
    for key1, value1 in callsmap.items():
        counter += len(value1)
    return counter


def get_callee_mapping(callee_array, func_map):
    array = []
    for item in callee_array:
        array.append(func_map[item])
    return array


def subtract_two_maps(map1, map2):
    keys = set(map1)
    map_added = {}
    map_removed = {}
    for key in keys:
        try:
            array1 = map1[key]
            array2 = map2[key]
        except Exception as e:
            print(e, 'error')
            continue
        set1 = set(array1)
        set2 = set(array2)
        added_calls = set1 - set2
        removed_calls = set2 - set1
        if len(added_calls) > 0:
            map_added[key] = list(added_calls)
        if len(removed_calls) > 0:
            map_removed[key] = list(removed_calls)
    return map_added, map_removed


def extract_maps(classes):
    classes_map = {}
    functions_map = {}
    calls_map = {}

    class_index = 0
    function_index = 0
    call_index = 0
    for class_item in classes:
        classes_map[class_item['class_name']] = class_index
        class_index += 1
        for function_item in class_item['functions']:
            functions_map[class_item['class_name'] + '.' + function_item['function_name']] = function_index
            function_index += 1
    error_counter = 0
    for class_item in classes:
        for function_item in class_item['functions']:
            for callee_item in function_item['calls']:
                call_index += 1
                try:
                    try:
                        callee_array = calls_map[
                            functions_map[class_item['class_name'] + '.' + function_item['function_name']]]
                    except:
                        callee_array = []
                    callee_array.append(functions_map[
                                            callee_item])
                    calls_map[
                        functions_map[class_item['class_name'] + '.' + function_item['function_name']]] = \
                        callee_array
                except Exception as e:
                    # print(e)
                    temp = str(e)
                    temp_parts = temp.split(".")[-1]
                    if not temp_parts[0].isupper() and not callee_item[0].isupper() and temp_parts[0] != '_':
                        # print(e, class_item['class_name'], callee_item)
                        error_counter += 1
                    continue
    return classes_map, functions_map, calls_map, class_index, function_index


vertex_changes_map = {}
vertex_bug_propagation_time_map = {}

path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\a6c110ebd05155fa5bdae4e2d195493d2d04dd4f\\"
classes = open(path + 'classes.txt').read()
classes = json.loads(classes)
main_classes_map, main_functions_map, main_calls_map, class_index, function_index = extract_maps(classes)
main_classes_map_copy = main_classes_map
main_functions_map_copy = main_functions_map
main_calls_map_copy = main_calls_map

for key, value in main_functions_map.items():
    vertex_changes_map[value] = {'psd': 0, 'pds': 0, 'psd_date': 0, 'pds_date': 0}
    vertex_bug_propagation_time_map[value] = []

print(len(main_classes_map), len(main_functions_map), get_callee_number(main_calls_map), 'init\n')
with open('C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\commits_list_new.txt') as commits_file:
    content = commits_file.readlines()
content.reverse()
index = 0
last_calls_map = {}
last_functions = []
prev_functions_diff_removed = 0

propagation_time_index = 0
propagation_time_total = 0
propagation_time_array = []
src_dst_array = []

with open('vertex_bug_changes_date_map.txt') as vertex_bug_changes_file:
    vertex_bug_changes_map = eval(vertex_bug_changes_file.read())

for commit in content:
    print(index, 'index\n')
    if commit.strip() == "a6c110ebd05155fa5bdae4e2d195493d2d04dd4f":
        print("continue")
        continue

    path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit.strip() + "\\"
    try:
        classes = open(path + 'classes.txt').read()
    except:
        continue

    classes = json.loads(classes)

    class_map = {}
    functions_map = {}
    calls_map = {}
    new_classes = []
    new_functions = []
    new_calls = []
    class_number = 0
    functions_number = 0
    calls_number = 0
    bug_number = 0
    key_exists = 0
    key_not_exists = 0
    for class_item in classes:
        class_number += 1
        try:
            class_map[class_item['class_name']] = main_classes_map[class_item['class_name']]
        except Exception as e:
            new_classes.append(class_item['class_name'])
            main_classes_map[class_item['class_name']] = class_index
            class_index += 1
    new_classes_set = set(new_classes)

    current_functions_array = []
    for class_item in classes:
        for function_item in class_item['functions']:
            functions_number += 1
            try:
                current_functions_array.append(
                    main_functions_map[class_item['class_name'] + '.' + function_item['function_name']])
                functions_map[class_item['class_name'] + '.' + function_item['function_name']] = main_functions_map[
                    class_item['class_name'] + '.' + function_item['function_name']]

            except Exception as e:
                new_functions.append(class_item['class_name'] + '.' + function_item['function_name'])
                main_functions_map[class_item['class_name'] + '.' + function_item['function_name']] = function_index
                current_functions_array.append(function_index)
                vertex_changes_map[function_index] = {'psd': 0, 'pds': 0, 'psd_date': 0, 'pds_date': 0}
                vertex_bug_propagation_time_map[function_index] = []
                function_index += 1

    added_functions = set(current_functions_array) - set(last_functions)
    removed_functions = set(last_functions) - set(current_functions_array)
    print(added_functions, 'added functions')
    print(removed_functions, 'removed functions')
    last_functions = current_functions_array

    for class_item in classes:
        for function_item in class_item['functions']:
            calls_number += 1
            try:
                callee_mapping = get_callee_mapping(
                    function_item['calls'], main_functions_map)
                calls_map[main_functions_map[
                    class_item['class_name'] + '.' + function_item['function_name']]] = callee_mapping

            except Exception as e:
                bug_number += 1
    added_calls, removed_calls = subtract_two_maps(calls_map, last_calls_map)

    text = ""

    for caller, callees in calls_map.items():

        for item in callees:
            if vertex_bug_changes_map[caller] and vertex_bug_changes_map[item]:
                date_array_source = vertex_bug_changes_map[caller]
                date_array_dst = vertex_bug_changes_map[item]
                date_diff = source_dst_date_diff(date_array_source, date_array_dst)
                if date_diff:
                    if not src_dst_exists(caller, item, vertex_bug_propagation_time_map):
                        insert_time_map(caller, item, date_diff, vertex_bug_propagation_time_map)
                        propagation_time_index += 1
                        propagation_time_total += date_diff
                        propagation_time_array.append(date_diff)
                        src_dst_array.append((caller, item))

    last_calls_map = calls_map
    print(bug_number, 'bug')

    print(commit)

    if index == 0:
        print(calls_map)
    index += 1

with open('vertex_bug_propagation_map_psd.txt', 'w') as vertex_bug_propagation_file:
    vertex_bug_propagation_file.write(str(vertex_bug_propagation_time_map))
# print(propagation_time_index, propagation_time_total, propagation_time_total/propagation_time_index)
print('median: ', my_statistics.median(propagation_time_array))
print('mode: ', my_statistics.mode(propagation_time_array))
print('mean: ', my_statistics.mean(propagation_time_array))
print('max: ', max(propagation_time_array))
print('min: ', min(propagation_time_array))
print('length: ', len(propagation_time_array))
print('array:', propagation_time_array)
print('src dst array', src_dst_array)
