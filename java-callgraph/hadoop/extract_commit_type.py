import os
import requests
import json

# for a, b, c in os.walk("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\commits"):
#     commit = a.split('\\')[-1]
#     try:
#         with open("C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit + "\\commit_type.txt") as file:
#             commit_type = file.read()
#         with open(a + "\\commit_type.txt", "w") as commit_type_file:
#             commit_type_file.write(commit_type)
#     except:
#         print(commit)
with open("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\no_commit_type_list.txt") as file:
    no_commit_type_list = file.readlines()

for commit in no_commit_type_list:
    path = "C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\\commits\\" + commit.strip() + "\\"

    try:
        commit_tag = open(path + 'commit_tag.txt').read()
    except:
        print("tag does not exist")
        continue
    r = ""
    if not os.path.isfile(path + "commit_type.txt"):
        try:
            r = requests.get('https://issues.apache.org/jira/rest/api/2/issue/' + commit_tag)
        except Exception as e:
            print(e, 'error')
            continue
        if r.content:
            try:
                issue_info = json.loads(r.content.decode('utf-8'))
                issue_type = issue_info['fields']['issuetype']['name']
                issue_status = issue_info['fields']['status']['name']
                text = issue_type + '\n'
                text += issue_status
                with open(path + "commit_type.txt", 'w') as commit_type:
                    commit_type.write(text)
            except Exception as e:
                print('error: ' + str(e))
