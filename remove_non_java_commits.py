import git

r = git.Repo("C:\\Users\\anaeimia\Documents\Thesis\Spark\spark")
commit = r.head.commit
parent = commit.parents[0]
index = 0
no_java_commits = []
# commit = r.commit("b84769a1073fde76a1a7efad51bf73ac1ee6db2a")
# parent = commit.parents[0]

while commit:
    files_array = []
    for item in commit.diff(parent):
        try:
            files_array.append(item.a_blob.path.split('.')[-1])
            # print(item.a_blob.path.split('.')[-1])
        except:
            continue
    if files_array.__contains__('java'):
        print(commit)
    else:
        no_java_commits.append(str(commit))
        index += 1
    commit = parent
    try:
        parent = commit.parents[0]
    except:
        break
print(index)
print(no_java_commits)
print(len(no_java_commits))