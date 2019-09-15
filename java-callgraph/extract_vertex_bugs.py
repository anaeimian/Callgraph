import os

# functions_map_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\functions_map_new.txt"
functions_map_path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\Analysis Results\spark_functions_map.txt"
# commits_path = "D:\jmeter\commits"
commits_path = "D:\spark_commits\\"
# vertex_bugs_map_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\\vertex_bugs_map_new.txt"
vertex_bugs_map_path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\Analysis Results\\vertex_bugs_map.txt"

vertex_bugs_map = {}

with open(functions_map_path) as functions_map_file:
    functions_map = eval(functions_map_file.read())
for func_item in functions_map.values():
    vertex_bugs_map[func_item] = {'commits': [], 'bugs': 0}
cnt=0
for a, b, c in os.walk(commits_path):
    commit = a.split("\\")[-1]
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
            # sign = line_parts[0]
            if length == 3:
                caller = int(line_parts[1])
                caller_list.add(caller)

        # New functions should be removed from the list since they are not buggy functions
        for line in diff:
            line_parts = line.strip().split(" ")
            length = len(line_parts)
            sign = line_parts[0]
            if length == 2 and sign == "+":
                caller = int(line_parts[1])
                try:
                    caller_list.remove(caller)
                    cnt += 1
                except Exception as e:
                    print(e)

        for caller_item in caller_list:
            caller_bugs = vertex_bugs_map[caller_item]
            if not caller_bugs['commits'].__contains__(commit):
                caller_bugs['commits'].append(commit)
            caller_bugs['bugs'] += 1
            vertex_bugs_map[caller_item] = caller_bugs
    except Exception as e:
        print("error", e)
        continue
with open(vertex_bugs_map_path, "w") as file:
    file.write(str(vertex_bugs_map))
print(cnt)