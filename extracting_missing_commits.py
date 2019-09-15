import os
with open("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\hadoop_core_java_commits.txt") as java_commits_file:
    java_commits = java_commits_file.readlines()

for a, b, c in os.walk("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\commits"):
    array = b
    break
# for commit in array:
#     try:
#         os.rmdir("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\commits\\"+commit)
#     except:
#         continue
for item in java_commits:
    if item.strip() == "deec7ca21ad1f7239b53f6dea36de043db13651b":
        break
    if item.strip() not in array:
        print(item.strip())

