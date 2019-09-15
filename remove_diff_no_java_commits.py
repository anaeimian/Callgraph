import os

with open('C:\\Users\\anaeimia\Documents\Thesis\Spark\Analysis Results\\no_java_commits.txt',
          'r') as no_java_commits_file:
    no_java_commits = no_java_commits_file.readlines()
index = 0
for commit in no_java_commits:
    try:
        stat_info = os.stat(
            'C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + commit.strip() + '\\new_diff.txt')

        if stat_info.st_size > 0:
            index += 1
            # print(stat_info.st_size)
            print(commit.strip())
            with open('C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\' + commit.strip() + '\\new_diff.txt', 'w') as diff_file:
                diff_file.write("")
    except:
        continue
print(index)
# with open ("C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\"+commit.strip()+"\\new_diff.txt") as
# print(commit.strip())
