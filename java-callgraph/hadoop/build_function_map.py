import os

# first snapshot: 36cedca874f21a37b5f69e077ea63484e1913a68
functions_map = {}
hadoop_functions_map = {}
with open('C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\parents_list.txt') as commits_file:
    parents_list = commits_file.readlines()
parents_list.reverse()

base_path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\commits\\"

commit1 = "36cedca874f21a37b5f69e077ea63484e1913a68"
path1 = base_path + commit1 + "\\"
with open(path1 + 'call_graph_map.txt', 'r') as callgraph1_file:
    call_graph1 = eval(callgraph1_file.read())
index = 0
hadoop_index = 0
for key, value in call_graph1.items():
    for function, callee_list in value.items():
        if not function.__contains__('<init>') and not function.__contains__('<clinit>') and not function.__contains__(
                "access$"):
            if not functions_map.__contains__(key + "." + function):
                functions_map[key + "." + function] = index
                index += 1
            if function.__contains__('org.apache.hadoop'):
                if not hadoop_functions_map.__contains__(key + "." + function):
                    hadoop_functions_map[key + "." + function] = hadoop_index
                    hadoop_index += 1
            for item in callee_list:
                if not item.__contains__('<init>') and not item.__contains__('<clinit>') and not item.__contains__(
                        "access$"):
                    if not functions_map.__contains__(item):
                        functions_map[item] = index
                        index += 1
                        if item.__contains__('org.apache.hadoop'):
                            if not hadoop_functions_map.__contains__(item):
                                hadoop_functions_map[item] = hadoop_index
                                hadoop_index += 1
# with open('C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\' + 'functions_map.txt', 'w') as call_graph_map_file:
#     call_graph_map_file.write(str(functions_map))
# print(hadoop_index)
# print(index)
# print(b)
with open('C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\hadoop_core_java_commits.txt') as commits_file:
    java_commits = commits_file.readlines()
for commit in parents_list:
    commit = commit.strip()
    if commit+"\n" in java_commits:
        print(commit)
