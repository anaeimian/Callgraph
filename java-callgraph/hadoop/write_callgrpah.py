import statistics
import json


def search_map(map1, value):
    for key, val in map1.items():
        if str(val) == str(value):
            return key


with open('C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\hadoop_functions_map.txt') as functions_map_file:
    functions_map = eval(functions_map_file.read())
index = len(functions_map.keys())
index += 1
with open(
        'C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\commits\\252c2b4d52e0dd8984d6f2a8f292f40e1c347fab\\new_call_graph_map.txt',
        'r') as callgraph_file:
    callgraph = eval(callgraph_file.read())
array = []
for key, value in callgraph.items():
    for function_item, callee_list in value.items():
        try:
            temp = functions_map[key + '.' + function_item]
        except:
            functions_map[key + '.' + function_item] = index
            index += 1
        print(functions_map[key + '.' + function_item])
        array.append(functions_map[key + '.' + function_item])
        for item in callee_list:
            print(functions_map[item])
            array.append(functions_map[item])
set1 = set(sorted(array))
print(set1)
csv_file = open("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\functions.txt", 'w')
function_names = []
for item in set1:
    csv_file.write(str(item) + ',' + search_map(functions_map, item)+'\n')
csv_file.close()
