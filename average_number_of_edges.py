import statistics
import json

basic_path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\\"
# basic_path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\\"
with open(basic_path + 'commits_list_new.txt') as commits_file:
    content = commits_file.readlines()
edges_array = []
for commit in content:
    path = basic_path + "\himrod docs\spark\\" + commit.strip() + "\\"
    # path = basic_path + "\hadoop\\" + commit.strip() + "\\"
    edges = 0
    try:
        call_graph = open(path + 'call_graph.txt').read()
        call_graph = json.loads(call_graph)
        for item in call_graph:
            edges += len(item['callee_list'])
        edges_array.append(edges)
        print(edges)
        edges = 0

    except:
        continue

print(statistics.mean(edges_array))
