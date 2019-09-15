import git

repository_path = "C:\\Users\\anaeimia\Documents\Thesis\jmeter\jmeter"
commits_path = "D:\jmeter\commits\\"
repository = git.Repo(repository_path)
commits = repository.iter_commits()
commit = repository.head.commit
while commit:
    commit_message = str(commit.message)
    commit_message = commit_message.strip()
    if commit_message[:3].lower() == "bug":
        bug_content = "Bug"
    else:
        bug_content = ""
    try:
        with open(commits_path + commit.hexsha + "\\commit_type.txt", "w") as commit_type_file:
            commit_type_file.write(bug_content)
    except Exception as e:
        print(e)
    commit = commit.parents[0]
