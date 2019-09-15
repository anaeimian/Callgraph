import git

base_path = "C:\\Users\\anaeimia\Documents\Thesis\hadoop_new_version\hadoop"
repo_directory_address = base_path
repository = git.Repo(repo_directory_address)
commit = repository.head.commit

index = 0
while commit.parents:
    parent = commit.parents[0]
    # print(len(commit.parents))
    commit = parent
    index += 1
    print(commit.committed_date)
