# This script uses vertex_bug_changes_date_map and edge_life_cycle_map and
# determines neighbor vertices which are buggy and determines the direction of bug propagation
import math


def edge_exists_in_graph(edge_info, src_date, dst_date):
    dates = edge_info['dates']
    changes = edge_info['changes']
    if changes[0] == "add":
        for index in range(math.floor(len(dates)/2)):
            if int(dates[2 * index]) <= src_date <= int(dates[2 * index + 1]) and int(dates[2 * index]) <= dst_date <= int(dates[
                    2 * index + 1]):
                return True
        if len(dates) % 2 == 1:
            if src_date >= int(dates[len(dates)-1]) and dst_date >= int(dates[len(dates)-1]):
                return True
    return False


i = 0
with open('edge_life_cycle_map.txt', 'r') as edge_life_cycle_map_file:
    edge_life_cycle_map = eval(edge_life_cycle_map_file.read())
with open('vertex_changes_map_dates_commits.txt', 'r') as vertex_bug_changes_file:
    vertex_bug_changes = eval(vertex_bug_changes_file.read())
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
        if edge_exists_in_graph(info, int(src_date_min), int(dst_date_min)):
            if src_date_min < dst_date_min:
                print(edge)
                i += 1
                print(src_commit.strip(), dst_commit.strip())

print(i)
