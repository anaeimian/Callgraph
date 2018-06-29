import json


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
            print(e, 'error',)
            # print(map1)
            continue
        set1 = set(array1)
        set2 = set(array2)
        added_calls = set1-set2
        removed_calls = set2-set1
        if len(added_calls) > 0:
            map_added[key] = list(added_calls)
        if len(removed_calls) > 0:
            map_removed[key] = list(removed_calls)
    return map_added, map_removed

# def get_calls_difference():


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
    # print(class_index, function_index, call_index)
    return classes_map, functions_map, calls_map, class_index, function_index


path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\a6c110ebd05155fa5bdae4e2d195493d2d04dd4f\\"
classes = open(path + 'classes.txt').read()
classes = json.loads(classes)
main_classes_map, main_functions_map, main_calls_map, class_index, function_index = extract_maps(classes)
main_classes_map_copy = main_classes_map
main_functions_map_copy = main_functions_map
main_calls_map_copy = main_calls_map
print(len(main_classes_map), len(main_functions_map), get_callee_number(main_calls_map), 'init\n')
with open('C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\commits_list_new.txt') as commits_file:
    content = commits_file.readlines()
content.reverse()
index = 0
last_calls_map = {}
last_functions = []
prev_functions_diff_removed = 0
in_degree_map = {}
out_degree_map = {}

for key, value in main_functions_map.items():
    in_degree_map[value] = 0
    out_degree_map[value] = 0

print(in_degree_map)
print(out_degree_map)
# content = []

for commit in content:
    # print(index, 'index\n')
    # if index != 1000:
    #     continue
    # else:
    #     # print(commit.)
    if commit.strip() == "a6c110ebd05155fa5bdae4e2d195493d2d04dd4f":
        print("continue")
        continue

    path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit.strip() + "\\"
    try:
        classes = open(path + 'classes.txt').read()
    except:
        continue
    #     hadoop_number -= 1
    #     print(index)

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
    # classes_diff_removed = set(main_classes_map) - set(class_map)
    # new_classes_set = new_classes_set | set(class_map)

    # break
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
                in_degree_map[function_index] = 0
                out_degree_map[function_index] = 0
                function_index += 1

    added_functions = set(current_functions_array)-set(last_functions)
    removed_functions = set(last_functions) - set(current_functions_array)
    # print(added_functions, 'added functions')
    # print(removed_functions, 'removed functions')
    last_functions = current_functions_array

    for class_item in classes:
        for function_item in class_item['functions']:
            calls_number += 1
            try:
                calls_map[main_functions_map[
                    class_item['class_name'] + '.' + function_item['function_name']]] = get_callee_mapping(
                    function_item['calls'], main_functions_map)
                out_degree_map[
                    main_functions_map[class_item['class_name'] + '.' + function_item['function_name']]] += len(
                    function_item['calls'])
                # in_degree_map[
                #     main_functions_map[class_item['class_name'] + '.' + function_item['function_name']]] += len(
                #     function_item['calls'])
            except Exception as e:
                bug_number += 1
    # added_calls, removed_calls = subtract_two_maps(calls_map, last_calls_map)
    # print(added_calls, 'added calls')
    # print(removed_calls, 'removed calls')
    # last_calls_map = calls_map
    # print(bug_number, 'bug')

    # if index == 1000:
    #     with open('middle_call_graph.txt', 'w') as middle_call_graph:
    #         middle_call_graph.write(str(calls_map))
    #
    # if index > 2500 and len(calls_map) > 10:
    #     with open('final_call_graph.txt', 'w') as final_call_graph:
    #         final_call_graph.write(str(calls_map))
    #     print("file index!")
    # index += 1

    # result_text = ""
    # for item in added_functions:
    #     result_text += "+ " + str(item) + " \n"
    # for item in removed_functions:
    #     result_text += "- " + str(item) + " \n"
    # for key, value in added_calls.items():
    #     for item in value:
    #         result_text += "+ " + str(key) + " " + str(item) + " \n"
    # for key2, value2 in removed_calls.items():
    #     for item2 in value2:
    #         result_text += "- " + str(key2) + " " + str(item2) + " \n"
    # with open(path + 'diff.txt', 'w') as diff:
    #     diff.write(result_text)
    # print(result_text)
    # print(commit)

    vertices_file = "id:ID,name:String,:Label\n"
    for key, value in main_functions_map.items():
        vertices_file += str(value) + "," + str(key) + ',function\n'
    with open(path + 'vertices.csv', 'w') as vertices:
        vertices.write(vertices_file)

    edges_file = "id:START_ID,id:END_ID,:type\n"
    for key, value in calls_map.items():
        for value_item in value:
            edges_file += str(key) + "," + str(value_item)+',call\n'
    with open(path + 'edges.csv', 'w') as edges:
        edges.write(edges_file)

# with open("classes_map.txt", 'w') as classes_map:
#     classes_map.write(str(main_classes_map))
# with open("functions_map.txt", 'w') as functions_map:
#     functions_map.write(str(main_functions_map))
# with open("calls_map.txt", 'w') as calls_map:
#     calls_map.write(str(main_calls_map))
