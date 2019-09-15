import os

vertex_bugs_map = {}
with open("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\hadoop_functions_map.txt") as functions_map_file:
    functions_map = eval(functions_map_file.read())
for func_item in functions_map.values():
    vertex_bugs_map[func_item] = {'commits': [], 'bugs': 0}
print(vertex_bugs_map)
for a, b, c in os.walk("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\commits\\"):
    commit = a.split("\\")[-1]
    if commit == "76be82bc0419affbe0103bc4f45c90926f08d0cc":
        continue
    caller_list = set()
    type = ""
    try:
        with open(a + "\\commit_type.txt") as file:
            type = file.readlines()[0].strip()
    except:
        continue

    if type != "Bug":
        continue
    try:
        with open(a + "\\diff.txt") as diff_file:
            diff = diff_file.readlines()
        for line in diff:
            line_parts = line.strip().split(" ")
            length = len(line_parts)
            sign = line_parts[0]
            if length == 3:
                caller = int(line_parts[1])
                caller_list.add(caller)

        for caller_item in caller_list:
            caller_bugs = vertex_bugs_map[caller_item]
            caller_bugs['commits'].append(commit)
            caller_bugs['bugs'] += 1
            vertex_bugs_map[caller_item] = caller_bugs
    except Exception as e:
        print("error", e)
        continue
with open("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\vertex_bugs_map.txt", "w") as file:
    file.write(str(vertex_bugs_map))
