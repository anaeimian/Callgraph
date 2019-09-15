# This file goes through the commits and extracts the commit date in two formats

import git
import time
import os

# repo_directory_address = 'C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop'
repo_directory_address = 'C:\\Users\\anaeimia\Documents\Thesis\Spark\spark'
repository = git.Repo(repo_directory_address)
# commits = list(repository.iter_commits(paths='C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop\hadoop-common-project\hadoop-common\src\main\java\org\\apache\hadoop'))
commits = list(repository.iter_commits())

# commit = repository.head.commit

index = 0
new_date_exists = False
# while commit.parents:
for commit in commits:
    path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\" + commit.hexsha + "\\"
    # path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit.hexsha + "\\"
    # for a, b, c in os.walk(path):
    #     if 'new_date.txt' not in c:
    #         print(commit)
    #         new_date_exists = True
    #         index+=1
    # if new_date_exists:
    #     new_date_exists = False
    #     continue
    # if commit.hexsha != "01e8f056d9b7245193e6050f9830ca058db02a6e":
    #     continue
    # print(commit.committed_date)
    if time.gmtime(commit.committed_date).tm_mon < 10:
        month = '0' + str(time.gmtime(commit.committed_date).tm_mon)
    else:
        month = str(time.gmtime(commit.committed_date).tm_mon)
    if time.gmtime(commit.committed_date).tm_mday < 10:
        day = '0' + str(time.gmtime(commit.committed_date).tm_mday)
    else:
        day = str(time.gmtime(commit.committed_date).tm_mday)
    date = str(commit.committed_date) + "\n"
    date += str(time.gmtime(commit.committed_date).tm_year) + "-" + month + "-" + day

    try:
        parent = commit.parents[0]
        commit = parent
    except Exception as e:
        print(e, 'err')

    try:
        with open((path + "date.txt"), 'w') as date_file:
            date_file.write(date)
    except Exception as e:
        print(e, "error")
        continue
print(index)

# text = ""
# # commits.reverse()
# for commit in commits:
#     if commit.hexsha != "68c07ea198df8649ac41b2bf527edbf4d5dda88d":
#         continue
#     else:
#         print(commit.committed_date)
#     if time.gmtime(commit.committed_date).tm_mon < 10:
#         month = '0' + str(time.gmtime(commit.committed_date).tm_mon)
#     else:
#         month = str(time.gmtime(commit.committed_date).tm_mon)
#     if time.gmtime(commit.committed_date).tm_mday < 10:
#         day = '0' + str(time.gmtime(commit.committed_date).tm_mday)
#     else:
#         day = str(time.gmtime(commit.committed_date).tm_mday)
#     date = str(commit.committed_date) + "\n"
#     date += str(time.gmtime(commit.committed_date).tm_year) + "-" + month + "-" + day
#     path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\" + commit.hexsha + "\\"
#     try:
#         with open((path + "date.txt"), 'w') as date_file:
#             date_file.write(date)
#     except Exception as e:
#         print(e, "error")
#         continue
