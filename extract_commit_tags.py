# This file extracts commit tag (which is used in Jira) from the beginning of commit message
import git

base_path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\\"
repo_directory_address = base_path + "spark"
repository = git.Repo(repo_directory_address)
commits = repository.iter_commits()
index = 0

# with open(base_path + 'parents_list.txt') as commits_file:
with open(base_path + 'commits_list_new.txt') as commits_file:
    content = commits_file.readlines()
for commit in commits:
    # print(commit)
    # if commit.hexsha+"\n" not in list(content):
    #     print('not in list')
    #     continue

    path = "D:\spark_commits\\" + commit.hexsha + "\\"
    commit_message = str(commit.message.strip())
    start_index = commit_message.find('[SPARK-')
    end_index = commit_message.find(']')
    if start_index != -1 and end_index != -1:
        commit_tag = commit_message[start_index+1: end_index]

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
        index += 1
print(index)
