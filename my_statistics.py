import os

improvement = 0
sub_task = 0
bug = 0
new_feature = 0
dependency_upgrade = 0
documentation = 0
test = 0
task = 0
other = 0
error = 0
total=0
for a, b, c in os.walk("C:\\Users\\anaeimia\Documents\Thesis\himrod_docs\hadoop"):
# for a, b, c in os.walk("C:\\Users\\anaeimia\Documents\Thesis\Spark\himrod docs\spark"):
    try:
        with open(a + "\\commit_type.txt") as commit_type_file:
            commit_type = commit_type_file.readlines()
        # print(commit_type[0])
        if commit_type[0].strip() == "New Feature":
            new_feature += 1
        elif commit_type[0].strip() == "Improvement":
            improvement += 1
        elif commit_type[0].strip() == "Sub-task":
            sub_task += 1
        elif commit_type[0].strip() == "Documentation":
            documentation += 1
        elif commit_type[0].strip() == "Dependency upgrade":
            dependency_upgrade += 1
        elif commit_type[0].strip() == "Bug":
            bug += 1
        elif commit_type[0].strip() == "Test":
            test += 1
        elif commit_type[0].strip() == "Task":
            task += 1
        else:
            print(commit_type[0])
            other += 1
        total+=1

    except:
        error += 1

print("New Feature: ", new_feature)
print("Improvement: ", improvement)
print("Bug: ", bug)
print("Sub-task: ", sub_task)
print("Documentation: ", documentation)
print("Dependency Upgrade: ", dependency_upgrade)
print("Test: ", test)
print("Task: ", task)
print("Other: ", other)
print("total: ", total)
