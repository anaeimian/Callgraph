# This file extracts commit tag (which is used in Jira) from the beginning of commit message
import git

repo_directory_address = 'C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop'
repository = git.Repo(repo_directory_address)
commits = repository.iter_commits(
    paths='C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop\hadoop-common-project\hadoop-common\src\main\java\org\\apache\hadoop')
index = 0

with open('C:\\Users\\anaeimia\PycharmProjects\CallGraph\missing_commits.txt') as commits_file:
    content = commits_file.readlines()
for commit in commits:
    if commit.hexsha+"\n" not in list(content):
        continue

    path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit.hexsha + "\\"
    if commit.message.strip()[:6] == "HADOOP":
        if commit.message.strip()[11] in ' ,.:':
            commit_tag = commit.message.strip()[:11]
        else:
            commit_tag = commit.message.strip()[:12]

        try:
            with open(path + "metadata.txt", 'w') as metadata:
                metadata.write(commit_tag)
        except Exception as e:
            continue

    else:

        try:
            with open((path + "metadata.txt"), 'w') as metadata:
                metadata.write("")
        except Exception as e:
            print(e, "error")
            continue
        index += 1
print(index)
