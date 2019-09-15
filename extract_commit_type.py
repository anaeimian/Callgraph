# This file extracts commit type by sending a request to JIRA API
import json
import requests
import os


with open('C:\\Users\\anaeimia\Documents\Thesis\Spark\commits_list_new.txt') as commits_file:
    content = commits_file.readlines()
content.reverse()
index = 0
last_calls_map = {}
last_functions = []
prev_functions_diff_removed = 0
in_degree_map = {}
out_degree_map = {}


for commit in content:
    # print(index, 'index\n')

    # if commit.strip() == "a6c110ebd05155fa5bdae4e2d195493d2d04dd4f":
    #     print("continue")
    #     index += 1
    #     continue

    # path = "C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + commit.strip() + "\\"
    path = "D:\spark_commits\\" + commit.strip() + "\\"

    try:
        commit_tag = open(path + 'metadata.txt').read()
    except:
        print("metadata does not exist")
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

        index += 1

