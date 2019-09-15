import statistics

with open(
        'C:\\Users\\anaeimia\PycharmProjects\Thesis\hadoop_vertex_changes_map_dates_commits.txt') as vertex_changes_map_file:
# with open(
#         'C:\\Users\\anaeimia\Documents\Thesis\Spark\Analysis Results\spark_vertex_changes_map_dates_commits.txt') as vertex_changes_map_file:
    vertex_changes_map = eval(vertex_changes_map_file.read())
array = []
# for key, value in vertex_changes_map.items():
#     if len(value['dates']) > 0:
#         array.append(len(value['dates']))
#     print(key, len(value['dates']))
# print(statistics.mean(array))
# print(len(array))
with open('spark_functions_map.txt', 'r') as functions_map_file:
    functions_map = eval(functions_map_file.read())
with open(
        'C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\9a013b255f301c557c3868dc1ad657202e9e7a67\\call_graph.txt') as call_graph_file:
# with open(
#         'C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\db0b06c6ea7412266158b1c710bdc8ca30e26430\\call_graph.txt') as call_graph_file:
    call_graph = eval(call_graph_file.read())
for item in call_graph:
    print(item['index'], len(item['callee_list']), len(vertex_changes_map[item['index']]['dates']))
