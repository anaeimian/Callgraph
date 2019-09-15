import os


def get_file_size(path):
    return os.stat(path).st_size


def is_file_empty(path):
    if get_file_size(path):
        return False
    return True


index = 0
for a, b, c in os.walk("C:\\Users\\anaeimia\Documents\Thesis\java-callgraph\commits\\"):
    commit = a.split("\\")[-1]
    try:
        print(get_file_size(a + '\\callgraph_file'))
        # if is_file_empty(a + '\\commit_type.txt'):
        #     print('a;ldkjfa;lsjdflasjdf')
        #     index += 1
    except Exception as e:
        print(commit)
        continue
print(index)