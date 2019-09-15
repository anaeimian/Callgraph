## This file records an array of buggy commit ids that changed a vertex (function) for that vertex.
import time
import json
from datetime import date
import statistics


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
    for key, value in time_map.items():
        for item in value:
            if key == src and item[0] == dst:
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


def get_callees(node1, call_graph1):
    callees_array = []
    for caller_item, callees_list in call_graph1.items():
        if node1 == caller_item:
            callees_array.append(callees_list)
    return callees_array


def get_callee_number(calls_map):
    counter = 0
    for key, value in calls_map.items():
        counter += len(value)
    return counter


def get_callee_mapping(callee_array, func_map):
    # print("get callee mapping")
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
basic_path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\\"
path = basic_path + "himrod docs\spark\\d107b3b910d8f434fb15b663a9db4c2dfe0a9f43\\"
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
with open(basic_path + 'parents_list.txt') as commits_file:
    content = commits_file.readlines()
content.reverse()
index = 0
last_calls_map = {}
last_functions = []
prev_functions_diff_removed = 0

propagation_time_index = 0
propagation_time_total = 0
propagation_time_array = []

in_degree_avg_array = []
out_degree_avg_array = []
buggy_in_degree_avg_array = []
buggy_out_degree_avg_array = []
bug_propagated_in_degree_avg_array = []
bug_propagated_out_degree_avg_array = []

with open('C:\\Users\\anaeimia\Documents\Thesis\Spark\Analysis Results\spark_vertex_changes_map_dates_commits.txt') as vertex_bug_changes_file:
    vertex_bug_changes_map = eval(vertex_bug_changes_file.read())

for commit in content:
    print(index, 'index\n')
    if commit.strip() == "d107b3b910d8f434fb15b663a9db4c2dfe0a9f43":
        print("continue")
        continue
    # if index < 2500:
    #     index+=1
    #     continue
    path = basic_path + "himrod docs\spark\\" + commit.strip() + "\\"
    try:
        classes = open(path + 'classes.txt').read()
        classes = json.loads(classes)
    except:
        continue



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
    # print(added_functions, 'added functions')
    # print(removed_functions, 'removed functions')
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
    in_degree_array = []
    out_degree_array = []
    buggy_in_degree_array = []
    buggy_out_degree_array = []
    bug_propagated_in_degree_array = []
    bug_propagated_out_degree_array = []
    for caller, callee_list in calls_map.items():
        in_degree_array.append(len(get_callers(caller, calls_map)))
        out_degree_array.append(len(callee_list))
        if vertex_bug_changes_map[caller]['dates']:
            buggy_in_degree_array.append(len(get_callers(caller, calls_map)))
            buggy_out_degree_array.append(len(callee_list))
        # for item in callee_list:
        #     if vertex_bug_changes_map[caller] and vertex_bug_changes_map[item]:
        #         buggy_in_degree_array.append(len(get_callers(item, calls_map)))
        #         buggy_out_degree_array.append(len(get_callees(item, calls_map)))
        #         date_array_source = vertex_bug_changes_map[caller]['dates']
        #         date_array_dst = vertex_bug_changes_map[item]
        #         date_diff = source_dst_date_diff(date_array_dst, date_array_source)
        #         if date_diff:
        #             if not src_dst_exists(caller, item, vertex_bug_propagation_time_map):
        #                 insert_time_map(caller, item, date_diff, vertex_bug_propagation_time_map)
        #                 propagation_time_index += 1
        #                 propagation_time_total += date_diff
        #                 propagation_time_array.append(date_diff)
        #                 bug_propagated_in_degree_array.append(len(get_callers(caller, calls_map)))
        #                 bug_propagated_out_degree_array.append(len(callee_list))
    if in_degree_array:
        in_degree_avg_array.append(statistics.mean(in_degree_array))
    if out_degree_array:
        out_degree_avg_array.append(statistics.mean(out_degree_array))

    if buggy_in_degree_array:
        buggy_in_degree_avg_array.append(statistics.mean(buggy_in_degree_array))
    if buggy_out_degree_array:
        buggy_out_degree_avg_array.append(statistics.mean(buggy_out_degree_array))

    if bug_propagated_in_degree_array:
        bug_propagated_in_degree_avg_array.append(statistics.mean(bug_propagated_in_degree_array))
    if bug_propagated_out_degree_array:
        bug_propagated_out_degree_avg_array.append(statistics.mean(bug_propagated_out_degree_array))

    last_calls_map = calls_map
    print(bug_number, 'bug')

    print(commit)
    index += 1


print("in degree average: ", statistics.mean(in_degree_avg_array))
print("out degree average: ", statistics.mean(out_degree_avg_array))

print("buggy in degree average: ", statistics.mean(buggy_in_degree_avg_array))
print("buggy out degree average: ", statistics.mean(buggy_out_degree_avg_array))

print("bug propagated in degree average: ", statistics.mean(bug_propagated_in_degree_avg_array))
print("bug propagated out degree average: ", statistics.mean(bug_propagated_out_degree_avg_array))

# with open(basic_path + 'Analysis Results\in_degree_avg_array.txt', 'w') as in_degree_avg_array_file:
#     in_degree_avg_array_file.write(str(in_degree_avg_array))
# with open('out_degree_avg_array.txt', 'w') as out_degree_avg_array_file:
#     out_degree_avg_array_file.write(str(out_degree_avg_array))
# with open('buggy_in_degree_avg_array.txt', 'w') as buggy_in_degree_avg_array_file:
#     buggy_in_degree_avg_array_file.write(str(buggy_in_degree_avg_array))
# with open('buggy_out_degree_avg_array.txt', 'w') as buggy_out_degree_avg_array_file:
#     buggy_out_degree_avg_array_file.write(str(buggy_out_degree_avg_array))
# with open('bug_propagated_in_degree_avg_array.txt', 'w') as bug_propagated_in_degree_avg_array_file:
#     bug_propagated_in_degree_avg_array_file.write(str(bug_propagated_in_degree_avg_array))
# with open('bug_propagated_out_degree_avg_array.txt', 'w') as bug_propagated_out_degree_avg_array_file:
#     bug_propagated_out_degree_avg_array_file.write(str(bug_propagated_out_degree_avg_array))
