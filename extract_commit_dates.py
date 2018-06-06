# This file goes through the commits and extracts the commit date in two formats

import git
import time

repo_directory_address = 'C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop'
repository = git.Repo(repo_directory_address)
commits = list(repository.iter_commits(
    paths='C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop\hadoop-common-project\hadoop-common\src\main\java\org\\apache\hadoop'))
text = ""
commits.reverse()
for commit in commits:
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
    path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit.hexsha + "\\"
    try:
        with open((path + "date.txt"), 'w') as date_file:
            date_file.write(date)
    except Exception as e:
        print(e, "error")
        continue
