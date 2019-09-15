import statistics
import json

# functions_map_path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\functions_map.txt"
# commit = "252c2b4d52e0dd8984d6f2a8f292f40e1c347fab"
# call_graph_path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\commits\\" + commit + "\\new_call_graph_map.txt"
# csv_nodes_path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\" + commit + "\\nodes.csv"
# csv_edges_path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\" + commit + "\\edges.csv"
# vertex_bugs_map_path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\vertex_bugs_map.txt"
# new_functions_map_path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\functions_map_new.txt"
functions_map_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\functions_map.txt"
commit = "f1208484e3a0ac9263d0e43e436ca7ad8fa1749f"
call_graph_path = "D:\jmeter\commits\\" + commit + "\\call_graph_map.txt"
csv_nodes_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\" + commit + "\\nodes.csv"
csv_edges_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\" + commit + "\\edges.csv"
vertex_bugs_map_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\vertex_bugs_map_new.txt"
new_functions_map_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\functions_map_new.txt"


def search_map(map1, value):
    for key, val in map1.items():
        if str(val) == str(value):
            return key


with open(vertex_bugs_map_path) as vertex_bugs_map_file:
    vertex_bugs_map = eval(vertex_bugs_map_file.read())

with open(functions_map_path) as functions_map_file:
    functions_map = eval(functions_map_file.read())

index = max(functions_map.values())
index += 1

with open(call_graph_path, 'r') as call_graph_file:
    call_graph = eval(call_graph_file.read())
nodes_array = []

edges_csv_file = open(csv_edges_path, 'w')
jmeter_functions = []
for key, value in call_graph.items():
    for function_item, callee_list in value.items():
        try:
            temp = functions_map[key + '.' + function_item]
        except:
            # print(key + '.' + function_item)
            functions_map[key + '.' + function_item] = index
            index += 1
        nodes_array.append(functions_map[key + '.' + function_item])

        if key.__contains__('org.apache.jmeter'):
            print(key + " " + str(functions_map[key + '.' + function_item]))
            print("hghghghghghghghghghghg")
            jmeter_functions.append(functions_map[key + '.' + function_item])
        for item in callee_list:
            try:
                temp = functions_map[item]
            except:
                functions_map[item] = index
                index += 1
            nodes_array.append(functions_map[item])
            if item.__contains__('org.apache.jmeter'):
                # print("aljkdhfkajsdhfkjshf")
                jmeter_functions.append(functions_map[key + '.' + function_item])
            # edges_csv_file.write(str(functions_map[key + '.' + function_item]) + ',' + str(functions_map[item]) + '\n')
edges_csv_file.close()
set1 = set(sorted(nodes_array))
nodes_csv_file = open(csv_nodes_path, 'w')
for item in set1:
    function_name = search_map(functions_map, item)
    try:
        bugs = str(vertex_bugs_map[item]['bugs'])
    except Exception as e:
        # print(e)
        bugs = 0
    # nodes_csv_file.write(
    #     str(item) + ';' + function_name + ';' + str(bugs) + '\n')
nodes_csv_file.close()

# with open(new_functions_map_path, 'w') as functions_map_file:
#     functions_map_file.write(str(functions_map))
print(list(set(sorted(jmeter_functions))))