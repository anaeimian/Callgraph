## This file records an array of buggy commit ids that changed a vertex (function) for that vertex.

import json


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
edge_life_cycle_map = {}

# path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\a6c110ebd05155fa5bdae4e2d195493d2d04dd4f\\"
# basic_path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\\"
basic_path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\\"
path = basic_path + "himrod docs\spark\\68c07ea198df8649ac41b2bf527edbf4d5dda88d\\"

classes = open(path + 'classes.txt').read()
classes = json.loads(classes)
main_classes_map, main_functions_map, main_calls_map, class_index, function_index = extract_maps(classes)
main_classes_map_copy = main_classes_map
main_functions_map_copy = main_functions_map
main_calls_map_copy = main_calls_map

for key, value in main_calls_map.items():
    for item in value:
        edge_life_cycle_map[(key, item)] = {'dates': [1367205573], 'changes': ['add'], 'commits': ['68c07ea198df8649ac41b2bf527edbf4d5dda88d']}

for key, value in main_functions_map.items():
    vertex_changes_map[value] = {'psd': 0, 'pds': 0, 'psd_date': 0, 'pds_date': 0}

print(len(main_classes_map), len(main_functions_map), get_callee_number(main_calls_map), 'init\n')
with open(basic_path + 'parents_list.txt') as commits_file:
    content = commits_file.readlines()
content.reverse()
index = 0
last_calls_map = {}
last_functions = []
prev_functions_diff_removed = 0

for commit in content:
    print(index, 'index\n')
    if commit.strip() == "68c07ea198df8649ac41b2bf527edbf4d5dda88d":
        print("continue")
        continue

    path = basic_path + "\himrod docs\spark\\" + commit.strip() + "\\"
    # path = basic_path + "\hadoop\\" + commit.strip() + "\\"
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

    try:
        commit_date = open(path + 'date.txt').readlines()[0].strip()
    except:
        commit_date = 0
        continue

    for key, value in removed_calls.items():
        for item in value:
            try:
                dates = edge_life_cycle_map[(key, item)]['dates']
            except:
                dates = []
            try:
                array = edge_life_cycle_map[(key, item)]['changes']
            except:
                array = []
            try:
                commits_array = edge_life_cycle_map[(key, item)]['commits']
            except:
                commits_array = []

            dates.append(commit_date)
            array.append('remove')
            commits_array.append(commit)
            edge_life_cycle_map[(key, item)] = {'dates': dates, 'changes': array, 'commits': commits_array}

    for key, value in added_calls.items():
        for item in value:
            try:
                dates = edge_life_cycle_map[(key, item)]['dates']
            except:
                dates = []
            try:
                array = edge_life_cycle_map[(key, item)]['changes']
            except:
                array = []

            try:
                commits_array = edge_life_cycle_map[(key, item)]['commits']
            except:
                commits_array = []

            dates.append(commit_date)
            commits_array.append(commit)
            array.append('add')
            edge_life_cycle_map[(key, item)] = {'dates': dates, 'changes': array, 'commits': commits_array}

    last_calls_map = calls_map
    print(bug_number, 'bug')

    print(commit)
    index += 1

with open(basic_path + 'Analysis Results\\new_edge_life_cycle_map.txt', 'w') as edge_life_cycle_map_file:
    edge_life_cycle_map_file.write(str(edge_life_cycle_map))
