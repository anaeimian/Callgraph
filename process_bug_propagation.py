with open('final_call_graph.txt', 'r') as inf:
    call_graph = eval(inf.read())
with open('vertex_bug_changes_date_map.txt', 'r') as vertex_bug_changes:
    vertex_changes = eval(vertex_bug_changes.read())
index = 0
for key, value in call_graph.items():
    flag = False
    for item in value:
        if vertex_changes[item]:
            flag = True
            break
    if vertex_changes[key] and flag:
        source_change_dates = vertex_changes[key]
        for item in value:
            found = False
            destination_change_dates = vertex_changes[item]
            for source_date in source_change_dates:
                for destination_date in destination_change_dates:
                    if source_date < destination_date:
                        print(key , item)
                        print(source_date, destination_date)
                        found = True
                        break
                if found:
                    break

        print("/////////////////////")
print(index)
