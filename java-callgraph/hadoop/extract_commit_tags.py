# This file extracts commit tag (which is used in Jira) from the beginning of commit message
import git

# import os
#
# for a, b, c in os.walk("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\commits"):
#     commit = a.split('\\')[-1]
#     try:
#         with open("C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit + "\\metadata.txt") as file:
#             commit_tag = file.read()
#         if commit_tag:
#             with open(a + "\\commit_tag.txt", "w") as commit_type_file:
#                 commit_type_file.write(commit_tag)
#     except:
#         print(commit)

with open("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\no_commit_tag_list_new.txt") as file:
    no_tag_commits = file.readlines()

base_path = "C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop"
repository = git.Repo(base_path)
commits = repository.iter_commits()
index = 0

# with open(base_path + 'parents_list.txt') as commits_file:
# with open(base_path + 'commits_list_new.txt') as commits_file:
#     content = commits_file.readlines()
for commit in commits:
    if commit.hexsha + '\n' not in list(no_tag_commits):
        continue

    path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\commits\\" + commit.hexsha + "\\"
    commit_message = str(commit.message.strip())
    start_index = commit_message.find('HDFS-')
    end_index = commit_message.find('.')
    if start_index != -1 and end_index != -1:
        commit_tag = commit_message[start_index: end_index]
        print(commit_tag, commit)
        try:
            with open(path + "commit_tag.txt", 'w') as metadata:
                metadata.write(commit_tag)
        except Exception as e:
            continue

    # else:
    #
    #     try:
    #         with open((path + "commit_tag.txt"), 'w') as metadata:
    #             metadata.write("")
    #     except Exception as e:
    #         print(e, "error")
    #     index += 1
print(index)
