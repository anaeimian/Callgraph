import git

repo_directory_address = 'C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop'
# repo_directory_address = 'C:\\Users\\anaeimia\Documents\Thesis\Spark\spark'
repository = git.Repo(repo_directory_address)
commit = repository.head.commit
parent = commit.parents[0]
index = 0
java_commits = set()
while commit:
    has_java = False
    for x in commit.diff(parent):
        try:
            # print(x.a_blob.path)
            if x.a_blob.path[-5:] == ".java" and not str(x.a_blob.path).__contains__('/test/') and str(
                    x.a_blob.path).__contains__('hadoop-common-project/hadoop-common/src/main/java/org/apache/hadoop'):
                has_java = True
                index += 1
                break
        except Exception as e:
            continue
    if has_java:
        print(commit)
        java_commits.add(commit)
    commit = parent
    try:
        parent = commit.parents[0]
    except:
        continue
print(index)
