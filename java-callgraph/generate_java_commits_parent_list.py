import git
repository_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\jmeter"
repository = git.Repo(repository_path)
commits = repository.iter_commits()

commit = repository.head.commit
parent = commit.parents[0]
while commit:
    for item in commit.diff(parent):
        if item.a_path.__contains__('.java') and item.a_path.__contains__('/core/'):
            print(commit)
            break
    commit = parent
    parent = commit.parents[0]
