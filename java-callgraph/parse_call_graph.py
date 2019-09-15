import os

commits_folder = "D:\jmeter\commits"
for a, b, c in os.walk(commits_folder):
    # if a.split("\\")[-1] != "442162048a1509aece5dc92e70e874674f648d58":
    #     continue
    try:
        with open(a + "\callgraph_file") as callgraph_file:
            callgraph = callgraph_file.readlines()
    except Exception as e:
        print(e)
        continue
    classes = set()
    classes_test = set()
    call_graph_map = {}
    for line in callgraph:
        line = line.strip()
        if line[0] == 'C':
            line_parts = line.split(' ')
            caller_class = line_parts[0][2:]
            callee_class = line_parts[1]
            classes.add(caller_class)
    for item in classes:
        call_graph_map[item] = {}
    for line in callgraph:
        line = line.strip()
        if line[0] == 'M':
            line_parts = line.split(' ')
            caller = line_parts[0]
            callee = line_parts[1]
            caller_class = caller.split(':')[1]
            caller_function = caller.split(':')[2]
            callee_class = callee.split(':')[0][3:]
            callee_function = callee.split(':')[1]
            if caller_function.__contains__('<init>') or caller_function.__contains__(
                    '<clinit>') or caller_function.__contains__(
                'access$') or callee_function.__contains__('<init>') or callee_function.__contains__(
                '<clinit>') or callee_function.__contains__('access$') or callee_function.__contains__('valueOf'):
                continue
            functions_map = call_graph_map[caller_class]
            caller_function_exists = False
            try:
                callee_array = functions_map[caller_function]
            except:
                callee_array = []
            if not callee_array.__contains__(callee_class + '.' + callee_function):
                callee_array.append(callee_class + '.' + callee_function)
                functions_map[caller_function] = callee_array

    with open(a + '\\call_graph_map.txt', 'w') as call_graph_map_file:
        call_graph_map_file.write(str(call_graph_map))
    print(a)
