# This file goes through the commits and extracts the commit date in two formats

import git
import time

# repo_directory_address = 'C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop'
repo_directory_address = 'C:\\Users\\anaeimia\Documents\Thesis\Spark\spark'
repository = git.Repo(repo_directory_address)
commits = list(repository.iter_commits())
text = ""
# commits.reverse()
for commit in commits:
    if commit.hexsha == "df29d0ea4c8b7137fdd1844219c7d489e3b0d9c9":
        break
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
    path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark\\" + commit.hexsha + "\\"
    try:
        with open((path + "date.txt"), 'w') as date_file:
            date_file.write(date)
    except Exception as e:
        print(e, "error")
        continue
