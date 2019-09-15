import networkx as nx

graph = nx.MultiDiGraph()



# functions_map_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\functions_map.txt"
# commit = "f1208484e3a0ac9263d0e43e436ca7ad8fa1749f"
# call_graph_path = "D:\jmeter\commits\\" + commit + "\\call_graph_map.txt"
# csv_nodes_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\" + commit + "\\nodes.csv"
# csv_edges_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\" + commit + "\\edges.csv"
# vertex_bugs_map_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\vertex_bugs_map_new.txt"
# new_functions_map_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\functions_map_new.txt"
#
#
# def search_map(map1, value):
#     for key, val in map1.items():
#         if str(val) == str(value):
#             return key
#
#
# with open(functions_map_path) as functions_map_file:
#     functions_map = eval(functions_map_file.read())
#
# index = max(functions_map.values())
# index += 1
#
# with open(call_graph_path, 'r') as call_graph_file:
#     call_graph = eval(call_graph_file.read())
# nodes_array = []
#
# edges_csv_file = open(csv_edges_path, 'w')
# jmeter_functions = []
# for key, value in call_graph.items():
#     for function_item, callee_list in value.items():
#         try:
#             temp = functions_map[key + '.' + function_item]
#         except:
#             # print(key + '.' + function_item)
#             functions_map[key + '.' + function_item] = index
#             index += 1
#         nodes_array.append(functions_map[key + '.' + function_item])
#
#         # if key.__contains__('org.apache.jmeter'):
#         #     jmeter_functions.append(functions_map[key + '.' + function_item])
#         for item in callee_list:
#             try:
#                 temp = functions_map[item]
#             except:
#                 functions_map[item] = index
#                 index += 1
#             nodes_array.append(functions_map[item])
#             # if item.__contains__('org.apache.jmeter'):
#                 # print("aljkdhfkajsdhfkjshf")
#                 # jmeter_functions.append(functions_map[key + '.' + function_item])
#             graph.add_edges_from([(functions_map[key + '.' + function_item],functions_map[item])])
# edges_csv_file.write(str(functions_map[key + '.' + function_item]) + ',' + str(functions_map[item]) + '\n')

# with open(new_functions_map_path, 'w') as functions_map_file:
#     functions_map_file.write(str(functions_map))
# graph.


for vertex in graph.nodes:
    print(vertex)


def BFS(tree, level=[1]):
    bfs_list = []
    if len(level) > 0:
        bfs_list += level
        sub_level = []
        for vertex in level:
            # if tree.__contains__(vertex):
            sub_level += tree[vertex]
        bfs_list += BFS(tree, sub_level)
    return bfs_list


a = {}
a[1] = [2, 3, 4]
a[2] = [3, 5]
a[3] = [6]
a[4] = []
a[5] = []
a[6] = []

graph.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2, 5), (3, 6)])

reachable_vertices = set(BFS(a, [1]))
reachable_vertices.remove(1)
print(reachable_vertices)
result = sum([(len(list(nx.all_simple_paths(graph, 1, item))) - 1) for item in reachable_vertices])

print(result)











# def traverse_graph(call_graph, temp_map, node):
#     if node not in call_graph.keys():
#         return 0
#     if not call_graph[node]:
#         return 0
#     total = 0
#     for callee in call_graph[node]:
#         temp_map[callee] = temp_map[node]
#     for callee in call_graph[node]:
#         callee_total = 0
#         callers = get_callers(call_graph, callee)
#         callers.remove(node)
#         # print(callee, callers,'callersssssssssssssssss', node)
#         for caller in callers:
#             callee_total += temp_map[caller]
#         temp_map[callee] += callee_total
#         # print(callee_total, 'callee_totallllllllllllllll', node)
#         total += temp_map[callee]
#     total -= len(call_graph[node])
#     print(temp_map, 'tmp map', node)
#
#     return total + sum([traverse_graph(call_graph, temp_map, callee_func) for callee_func in call_graph[node]])
#
#
# def get_callers(call_graph, node):
#     callers = []
#     for key, value in call_graph.items():
#         if node in value:
#             callers.append(key)
#     return callers
#
#
# a = dict()
# a[1] = [2, 3, 4]
# a[2] = [3, 5]
# a[3] = [6]
# main_set = set()
# main_map = {}
# for key, value in a.items():
#     main_set.add(key)
#     for item in value:
#         main_set.add(item)
# for item in main_set:
#     main_map[item] = 0
#
# for key, value in a.items():
#     temp_map = {}
#     for func_id, paths in main_map.items():
#         temp_map[func_id] = 0
#     temp_map[key] = 1
#     print(temp_map, key)
#     print(key, traverse_graph(a, temp_map, key))
#
