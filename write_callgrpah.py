import statistics
import json


def search_map(map1, value):
    for key, val in map1.items():
        if str(val) == str(value):
            return key


with open('hadoop_new_functions_map.txt', 'r') as functions_map_file:
    functions_map = eval(functions_map_file.read())

with open('hadoop_vertex_changes_map_dates_commits.txt') as vertex_bugs_file:
    vertex_info_map = eval(vertex_bugs_file.read())

basic_path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\\"
with open(basic_path + 'commits_list_new.txt') as commits_file:
    content = commits_file.readlines()
edges_array = []
# path = basic_path + "\hadoop\\0111711d8b2355a12a3e5f4da7f5a91e89355c1b\\"

path = basic_path + "\hadoop\\2eba7eb9aff5f7a1bf63ff1ebbe28d21fd37065b\\"
with open(path + "new_date.txt") as new_date:
    date = int(new_date.readlines()[0])
edges = 0
call_graph = open(path + 'call_graph.txt').read()
call_graph = json.loads(call_graph)
nodes = set()
for item in call_graph:
    for callee in item['callee_list']:
        try:
            # nodes.add(functions_map[item['function_name']])
            # nodes.add(functions_map[callee])
            print(str(functions_map[item['function_name']]) + ',' + str(functions_map[callee]))
        except Exception as e:
            continue
# for key, value in functions_map.items():
# for item in nodes:
#     counter = 0
#     changes = vertex_info_map[item]
#     for change in changes['dates']:
#         if int(change) > date:
#             counter += 1
#     print(str(item) + ',' + str(search_map(functions_map, item)) + ',' + str(counter))
