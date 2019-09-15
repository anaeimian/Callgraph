import git

with open('C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\parents_list.txt') as commits_file:
    content = commits_file.readlines()
content.reverse()
length = len(content)
i = 0
while content[i]:
    if content[i].strip() == "5128a9a453d64bfe1ed978cf9ffed27985eeef36":
        break
    i += 1
i += 1
while content[i] and i < length - 1:
    try:
        with open("C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop\\" + content[i].strip() + "\\diff_new.txt",
                  "r") as diff_file:
            diff = diff_file.readlines()
            for item in diff:
                parts = item.split(" ")
                if str(parts[2].strip()) == '6466' or str(parts[1].strip()) == '6466':
                    print(content[i].strip())
    except Exception as e:
        error = e
        # print(error)

    i += 1
