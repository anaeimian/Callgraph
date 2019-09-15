# first snapshot: 36cedca874f21a37b5f69e077ea63484e1913a68


with open('C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\hadoop_functions_map.txt') as functions_map_file:
    functions_map = eval(functions_map_file.read())
index = max(list(functions_map.values()))
index += 1
with open('C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\backup\commits_list_altered.txt') as commits_file:
    commits = commits_file.readlines()
base_path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\commits\\"
i = 0
while i < len(commits) - 1:
    commit1 = commits[i].strip()
    commit2 = commits[i + 1].strip()
    i += 1
    print(commit1)
    print(commit2)
    # commit1 = "fea16a440d195f1b4e03a62c9249e3518cea23b5"
    # commit2 = "252c2b4d52e0dd8984d6f2a8f292f40e1c347fab"
    path1 = base_path + commit1 + "\\"
    path2 = base_path + commit2 + "\\"
    with open(path1 + 'new_call_graph_map.txt', 'r') as callgraph1_file:
        call_graph1 = eval(callgraph1_file.read())
    try:
        with open(path2 + 'new_call_graph_map.txt', 'r') as callgraph2_file:
            call_graph2 = eval(callgraph2_file.read())
    except Exception as e:
        print(e)
        break

    classes_set1 = set(call_graph1.keys())
    classes_set2 = set(call_graph2.keys())

    added_classes = classes_set2 - classes_set1
    removed_classes = classes_set1 - classes_set2
    # print(added_classes)
    # print(removed_classes)
    added_functions_text = ""
    removed_functions_text = ""
    added_calls_text = ""
    removed_calls_text = ""
    for key, value in call_graph1.items():
        value1 = value
        try:
            value2 = call_graph2[key]
        except:
            value2 = {}
        functions_set1 = value1.keys()
        functions_set2 = value2.keys()

        added_functions = functions_set2 - functions_set1
        removed_functions = functions_set1 - functions_set2

        for item in added_functions:
            try:
                temp = functions_map[key + '.' + item]
            except:
                functions_map[key + '.' + item] = index
                index += 1
            added_functions_text += "+ " + str(functions_map[key + '.' + item]) + "\n"

        for item in removed_functions:
            try:
                temp = functions_map[key + '.' + item]
            except:
                functions_map[key + '.' + item] = index
                index += 1
            removed_functions_text += "- " + str(functions_map[key + '.' + item]) + "\n"
        for added_function in added_functions:
            added_function_callee_list = value2[added_function]
            for item in added_function_callee_list:
                added_calls.add(item)
            for item in added_calls:
                try:
                    temp = functions_map[item]
                    added_calls_text += "+ " + str(functions_map[key + '.' + added_function]) + " " + str(
                        functions_map[item]) + "\n"
                except:
                    functions_map[item] = index
                    added_calls_text += "+ " + str(functions_map[key + '.' + added_function]) + " " + str(
                        functions_map[item]) + "\n"
                    index += 1
        for func, callee_list in value1.items():
            callee_list1 = callee_list
            if func not in removed_functions:
                callee_list2 = value2[func]
                added_calls = set(callee_list2) - set(callee_list1)
                removed_calls = set(callee_list1) - set(callee_list2)
            else:
                added_calls = set()
                removed_calls = set(callee_list1)

            for item in added_calls:

                try:
                    temp = functions_map[key + '.' + func]
                except:
                    functions_map[key + '.' + func] = index
                    index += 1

                try:
                    temp = functions_map[item]
                except:
                    functions_map[item] = index
                    index += 1
                added_calls_text += "+ " + str(functions_map[key + '.' + func]) + " " + str(
                    functions_map[item]) + "\n"

            for item in removed_calls:
                try:
                    temp = functions_map[key + '.' + func]
                except:
                    functions_map[key + '.' + func] = index
                index += 1
                removed_calls_text += "- " + str(functions_map[key + '.' + func]) + " " + str(
                    functions_map[item]) + "\n"
        for added_function in added_functions:
            added_function_callee_list = value2[added_function]
            for item in added_function_callee_list:
                added_calls.add(item)

    text = ""
    if added_functions_text:
        text += added_functions_text
    if removed_functions_text:
        text += removed_functions_text
    if added_calls_text:
        text += added_calls_text
    if removed_calls_text:
        text += removed_calls_text
    with open(base_path + commit2 + "\\diff.txt", "w") as diff_file:
        diff_file.write(text)

# with open("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\hadoop_functions_map.txt",
#           "w") as new_functions_map_file:
#     new_functions_map_file.write(str(functions_map))
