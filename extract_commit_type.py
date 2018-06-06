# This file extracts commit type by sending a request to JIRA API
import json
import requests


def get_callee_number(calls_map):
    counter = 0
    for key, value in calls_map.items():
        counter += len(value)
    return counter


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
                    temp = str(e)
                    temp_parts = temp.split(".")[-1]
                    if not temp_parts[0].isupper() and not callee_item[0].isupper() and temp_parts[0] != '_':
                        error_counter += 1
                    continue
    return classes_map, functions_map, calls_map, class_index, function_index


path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\a6c110ebd05155fa5bdae4e2d195493d2d04dd4f\\"
classes = open(path + 'classes.txt').read()
classes = json.loads(classes)
main_classes_map, main_functions_map, main_calls_map, class_index, function_index = extract_maps(classes)
main_classes_map_copy = main_classes_map
main_functions_map_copy = main_functions_map
main_calls_map_copy = main_calls_map
print(len(main_classes_map), len(main_functions_map), get_callee_number(main_calls_map), 'init\n')
with open('C:\\Users\\anaeimia\PycharmProjects\CallGraph\missing_commits.txt') as commits_file:
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

for commit in content:
    print(index, 'index\n')

    if commit.strip() == "a6c110ebd05155fa5bdae4e2d195493d2d04dd4f":
        print("continue")
        index += 1
        continue

    path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit.strip() + "\\"

    try:
        commit_tag = open(path + 'metadata.txt').read()
    except:
        continue
    r = ""
    try:
        r = requests.get('https://issues.apache.org/jira/rest/api/2/issue/' + commit_tag)
    except:
        continue
    if r.content:
        issue_info = json.loads(r.content.decode('utf-8'))
        try:
            issue_type = issue_info['fields']['issuetype']['name']
            issue_status = issue_info['fields']['status']['name']
            text = issue_type + '\n'
            text += issue_status
            with open(path + "commit_type.txt", 'w') as commit_type:
                commit_type.write(text)
        except Exception as e:
            print('error: ' + str(e))

