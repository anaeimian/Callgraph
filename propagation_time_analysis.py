## This file records an array of buggy commit ids that changed a vertex (function) for that vertex.
import time
import json
from datetime import date


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


def get_callers(node, call_graph):
    callers = []
    for caller, callees in call_graph.items():
        if node in callees:
            callers.append(caller)
    return callers


def get_callee_number(calls_map):
    counter = 0
    for key, value in calls_map.items():
        counter += len(value)
    return counter


def get_callee_mapping(callee_array, functions_map):
    array = []
    for item in callee_array:
        array.append(functions_map[item])
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

path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\a6c110ebd05155fa5bdae4e2d195493d2d04dd4f\\"
classes = open(path + 'classes.txt').read()
classes = json.loads(classes)
main_classes_map, main_functions_map, main_calls_map, class_index, function_index = extract_maps(classes)
main_classes_map_copy = main_classes_map
main_functions_map_copy = main_functions_map
main_calls_map_copy = main_calls_map

for key, value in main_functions_map.items():
    vertex_changes_map[value] = {'psd': 0, 'pds': 0, 'psd_date': 0, 'pds_date': 0}

print(len(main_classes_map), len(main_functions_map), get_callee_number(main_calls_map), 'init\n')
with open('C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\commits_list_new.txt') as commits_file:
    content = commits_file.readlines()
content.reverse()
index = 0
last_calls_map = {}
last_functions = []
prev_functions_diff_removed = 0

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
                    text += str(caller) + " " + str(item) + " " + str(date_diff) + "\n"
    with open("temp\\" + str(commit.strip()) + ".txt", 'w') as file:
        file.write(text)

    last_calls_map = calls_map
    print(bug_number, 'bug')

    print(commit)
    index += 1

with open('vertex_changes_dic.txt', 'w') as vertex_changes_file:
    vertex_changes_file.write(str(vertex_changes_map))
text = ""
psd_total = 0
pds_total = 0
new_index = 0
for key, value in vertex_changes_map.items():
    text += str(key) + " psd: " + str(value['psd']) + " pds: " + str(value['pds']) + "\n"
    psd_total += value['psd']
    pds_total += value['pds']
    new_index += 1
text += "pds average:" + str(pds_total / new_index) + "\n"
text += "psd average:" + str(psd_total / new_index) + "\n"
with open('vertex_changes_map_new.txt', 'w') as vertex_changes_map_file:
    vertex_changes_map_file.write(str(text))
