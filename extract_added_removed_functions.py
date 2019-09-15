import os
from datetime import date
import numpy as np
import statistics


def search_map(map1, value):
    for key, val in map1.items():
        if str(val) == str(value):
            return key


def get_date(commit_id):
    with open("C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit_id + "\\new_date.txt") as date_file:
        return date_file.readlines()[1].strip()


def added_commit(removed_function, removed_commit):
    with open('C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\parents_list.txt') as commits_file1:
        content1 = commits_file1.readlines()
    content1.reverse()
    commits_array = []
    for commit in content1:
        if commit.strip() == removed_commit:
            break
        try:
            with open(
                    "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit.strip() + "\diff_new.txt") as diff_file1:
                diffs1 = diff_file1.readlines()
        except:
            continue
        for line1 in diffs1:
            line_parts1 = line1.split(" ")
            if len(line_parts1) == 3:
                if line_parts1[1].strip() == removed_function:
                    commits_array.append(commit.strip())
                    # return commit.strip()

    return commits_array


index = 0
with open('hadoop_new_functions_map.txt', 'r') as functions_map_file:
    functions_map = eval(functions_map_file.read())

date_diffs_array = []

for a, b, c in os.walk("C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop"):
    if "diff_new.txt" in c:
        flag = False
        src_vertices = []
        dst_vertices = []
        with open(a + "\diff_new.txt") as diff_file:
            diffs = diff_file.readlines()
        for line in diffs:
            line_parts = line.split(" ")
            if len(line_parts) == 3:
                if line_parts[0] == "-":
                    print(line_parts[1], search_map(functions_map, line_parts[1]))
                    for commit in added_commit(line_parts[1].strip(), a.split("\\")[-1].strip()):
                        date1 = get_date(commit)
                        print('+ ', commit, date1)
                    date1_parts = date1.split('-')
                    date2 = get_date(a.split("\\")[-1])
                    date2_parts = date2.split('-')
                    print('- ', a.split("\\")[-1], date2)
                    print((date(int(date2_parts[0]), int(date2_parts[1]), int(date2_parts[2])) - date(
                        int(date1_parts[0]), int(date1_parts[1]),
                        int(date1_parts[2]))).days)
                    date_diffs_array.append((date(int(date2_parts[0]), int(date2_parts[1]), int(date2_parts[2])) - date(
                        int(date1_parts[0]), int(date1_parts[1]),
                        int(date1_parts[2]))).days)
                    print()
print('length: ', len(date_diffs_array))
print('0.25 percentile adds-removes array: ', np.percentile(date_diffs_array, 25))
print('0.5 percentile adds-removes array: ', np.percentile(date_diffs_array, 50))
print('0.75 percentile adds-removes array: ', np.percentile(date_diffs_array, 75))
print('Mean: ', statistics.mean(date_diffs_array))
print('Mode: ', statistics.mode(date_diffs_array))
print(date_diffs_array)