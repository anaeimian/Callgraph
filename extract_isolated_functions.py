import os


def search_map(map1, value):
    for key, val in map1.items():
        if str(val) == str(value):
            return key


index = 0
with open('hadoop_new_functions_map.txt', 'r') as functions_map_file:
    functions_map = eval(functions_map_file.read())

for a, b, c in os.walk("C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop"):
    if "diff_new.txt" in c:
        flag = False
        src_vertices = []
        dst_vertices = []
        with open(a + "\diff_new.txt") as diff_file:
            diffs = diff_file.readlines()
        for line in diffs:
            line_parts = line.split(" ")
            if len(line_parts) > 3:
                src_vertices.append(line_parts[1].strip())
                dst_vertices.append(line_parts[2].strip())
        for line in diffs:
            line_parts = line.split(" ")
            if len(line_parts) == 3:
                if line_parts[1].strip() not in src_vertices and line_parts[1].strip() not in dst_vertices:
                    print(line_parts[0].strip(), line_parts[1].strip(), search_map(functions_map, line_parts[1]))
                    flag = True
        if flag:
            index += 1
            print(a.split("\\")[-1])
            print()
            print()
print(index)