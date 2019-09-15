import csv

csvfile = open('nodes.csv')
nodes = csv.reader(csvfile, delimiter=',', quotechar='|')

cyclomatic = open('cyclomatic.csv')
cyc = csv.reader(cyclomatic, delimiter=',', quotechar='|')
names1 = []
names2 = []
cyc_map = {}
for row in nodes:
    names1.append(str(row[1]))
for row1 in cyc:
    cyc_map[row1[1].replace('"', '') + '()'] = row1[2]
print(names1)

for item1 in names1:
    try:
        print(cyc_map[item1])
    except:
        print(0)
