import os

# first snapshot: 36cedca874f21a37b5f69e077ea63484e1913a68
functions_map = {}
hadoop_functions_map = {}
# with open('C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\parents_list.txt') as commits_file:
#     parents_list = commits_file.readlines()
# parents_list.reverse()

base_path = "D:\jmeter\commits\\"

commit1 = "1dc96508ae6d6a16173db86d92e67af0a3ccde4d"
path1 = base_path + commit1 + "\\"
with open(path1 + 'call_graph_map.txt', 'r') as callgraph1_file:
    call_graph1 = eval(callgraph1_file.read())
index = 0
hadoop_index = 0
for key, value in call_graph1.items():
    for function, callee_list in value.items():
        if not function.__contains__("org.apache.jmeter"):
            continue
        if function.__contains__('<init>') or function.__contains__('<clinit>') or function.__contains__(
                "access$"):
            continue
        if not functions_map.__contains__(key + "." + function):
            functions_map[key + "." + function] = index
            index += 1
        for item in callee_list:
            if item.__contains__('<init>') or item.__contains__('<clinit>') or item.__contains__(
                    "access$"):
                continue
            if not item.__contains__("org.apache.jmeter"):
                continue
            if not functions_map.__contains__(item):
                functions_map[item] = index
                index += 1
with open('C:\\Users\\anaeimia\Documents\Thesis\jmeter\\' + 'functions_map.txt', 'w') as call_graph_map_file:
    call_graph_map_file.write(str(functions_map))