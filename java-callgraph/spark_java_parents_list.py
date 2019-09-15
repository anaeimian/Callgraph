import git

repository_path = "C:\\Users\\anaeimia\Documents\Thesis\Spark\spark"
# commits_path = "D:\jmeter\commits\\"
repository = git.Repo(repository_path)
commits = repository.iter_commits()
commit = repository.head.commit

parent = commit.parents[0]
while commit:
    for item in commit.diff(parent):
        if item.a_path.__contains__('.java') and not item.a_path.__contains__('/test/'):
            print(commit)
            break
    commit = parent
    parent = commit.parents[0]