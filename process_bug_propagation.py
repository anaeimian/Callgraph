# This script uses vertex_bug_changes_date_map and edge_life_cycle_map and
# determines neighbor vertices which are buggy and determines the direction of bug propagation
import math


# def edge_exists_in_graph(src_vertex, dst_vertex):
#     with open('C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + src_commit.strip() + '\\call_graph.txt') as src_call_graph_file:
#         src_call_graph = eval(src_call_graph_file.read())
#     with open('C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + dst_commit.strip() + '\\call_graph.txt') as dst_call_graph_file:
#         dst_call_graph = eval(dst_call_graph_file.read())
#
#     for src_item in src_call_graph:
#         if src_item['function_name'] == search_map(functions_map, src_vertex):
#             if search_map(functions_map, dst_vertex) in src_item['callee_list']:
#             return True
#
#     # dates = edge_info['dates']
#     # changes = edge_info['changes']
#     # if changes[0] == "add":
#     #     for index in range(math.floor(len(dates) / 2)):
#     #         if int(dates[2 * index]) < src_date < int(dates[2 * index + 1]) and int(dates[2 * index]) < dst_date < int(
#     #                 dates[
#     #                     2 * index + 1]):
#     #             return True
#     #     if len(dates) % 2 == 1:
#     #         if src_date > int(dates[len(dates) - 1]) and dst_date > int(dates[len(dates) - 1]):
#     #             return True
#     return False


def search_map(map1, value):
    for key, val in map1.items():
        if str(val) == str(value):
            return key


i = 0
# with open('C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\Analysis Results\\hadoop_edge_life_cycle_map.txt', 'r') as edge_life_cycle_map_file:
with open('C:\\Users\\anaeimia\Documents\Thesis\Spark\Analysis Results\\spark_edge_life_cycle_map.txt', 'r') as edge_life_cycle_map_file:
    edge_life_cycle_map = eval(edge_life_cycle_map_file.read())
# with open('hadoop_vertex_changes_map_dates_commits.txt', 'r') as vertex_bug_changes_file:
with open('spark_vertex_changes_map_dates_commits_all_types.txt', 'r') as vertex_bug_changes_file:
    vertex_bug_changes = eval(vertex_bug_changes_file.read())
with open('spark_functions_map.txt', 'r') as functions_map_file:
    functions_map = eval(functions_map_file.read())

for edge, info in edge_life_cycle_map.items():
    src_vertex = edge[0]
    dst_vertex = edge[1]
    edge_dates = info['dates']
    src_date_array = vertex_bug_changes[src_vertex]['dates']
    dst_date_array = vertex_bug_changes[dst_vertex]['dates']
    if len(src_date_array) > 0 and len(dst_date_array) > 0:
        src_date_min = src_date_array[0]
        dst_date_min = dst_date_array[0]
        src_commit = vertex_bug_changes[src_vertex]['commits'][0]
        dst_commit = vertex_bug_changes[dst_vertex]['commits'][0]
        # if edge_exists_in_graph(info, int(src_date_min), int(dst_date_min)) or True:

        with open(
                'C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + src_commit.strip() + '\\new_diff.txt') as src_diff_file:
            src_diff = src_diff_file.readlines()
        with open(
                'C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + dst_commit.strip() + '\\new_diff.txt') as dst_diff_file:
            dst_diff = dst_diff_file.readlines()
        dst_in_src_diff = False
        dst_in_dst_diff = False

        for line in src_diff:
            line_parts = line.split(" ")
            # print(line_parts[1], dst_vertex)
            if len(line_parts) > 3 and str(line_parts[2]) == str(dst_vertex):
                dst_in_src_diff = True
                break
        if dst_in_src_diff:
            continue
        for line in dst_diff:
            line_parts = line.split(" ")
            if len(line_parts) > 3 and str(line_parts[2]) == str(dst_vertex):
                dst_in_dst_diff = True
                break
        if dst_in_dst_diff:
            continue

        has_src_changes = False
        has_dst_changes = False
        for line in src_diff:
            line_parts = line.split(" ")
            if str(line_parts[1]) == str(src_vertex):
                has_src_changes = True
                # print("true", src_vertex)
                break
        for line in dst_diff:
            line_parts = line.split(" ")
            if str(line_parts[1]) == str(dst_vertex):
                has_dst_changes = True
                # print("trueee", src_vertex)
                break
        if not has_src_changes or not has_dst_changes:
            continue
        # print(src_date_min, dst_date_min)
        # if edge_exists_in_graph(src_vertex, dst_vertex) or True:
        if src_date_min > dst_date_min:
            # print(src_date_min, dst_date_min)
            print(edge)
            print(search_map(functions_map, src_vertex),
                  search_map(functions_map, dst_vertex))
            print()

            print(src_commit.strip(), dst_commit.strip())
            with open(
                    'C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + src_commit.strip() + '\\commit_type.txt') as src_commit_type_file:
                src_commit_type = src_commit_type_file.readlines()

            with open(
                    'C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + dst_commit.strip() + '\\commit_type.txt') as dst_commit_type_file:
                dst_commit_type = dst_commit_type_file.readlines()

            print(src_commit_type[0].strip(), dst_commit_type[0].strip())
            # with open(
            #         'C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\' + src_commit.strip() + '\diff_new.txt') as src_diff_file:
            #     src_diff = src_diff_file.readlines()
            # with open(
            #         'C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\' + dst_commit.strip() + '\diff_new.txt') as dst_diff_file:
            #     dst_diff = dst_diff_file.readlines()
            with open(
                    'C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + src_commit.strip() + '\\new_diff.txt') as src_diff_file:
                src_diff = src_diff_file.readlines()
            with open(
                    'C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + dst_commit.strip() + '\\new_diff.txt') as dst_diff_file:
                dst_diff = dst_diff_file.readlines()

            for line in src_diff:
                line_parts = line.split(" ")
                if len(line_parts) > 3 and str(line_parts[1]) == str(src_vertex):
                    print("source: " + line_parts[0] + " " + str(search_map(functions_map, line_parts[2])))
            for line in dst_diff:
                line_parts = line.split(" ")
                if len(line_parts) > 3 and str(line_parts[1]) == str(dst_vertex):
                    print("destination: " + line_parts[0] + " " + str(search_map(functions_map, line_parts[2])))

            print()
            i += 1

print(i)
