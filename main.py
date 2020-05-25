class ClassSection:
    def __init__(self, name, units, start_time, end_time):
        self.name = name
        self.units = units
        self.start_time = start_time
        self.end_time= end_time

    def __str__(self):
        return "{} ({} units) / {}-{}".format(self.name, self.units, self.start_time, self.end_time)


def last_non_conflict(class_list:list, item_index:int) -> int:
    for i in range(item_index-1, 0, -1):
        if class_list[i].end_time <= class_list[item_index].start_time:
            return i

classes = [
    ClassSection('G', 2, 10, 12),
    ClassSection('A', 3, 8, 10),
    ClassSection('I', 3, 14, 16),
    ClassSection('C', 2, 8, 9),
    ClassSection('F', 3, 11, 13),
    ClassSection('B', 3, 9, 11),
    ClassSection('E', 3, 10, 12),
    ClassSection('H', 2, 11, 12),
    ClassSection('D', 2, 10, 11)
]

classes.sort(key=lambda item: (item.end_time, item.start_time))
n = len(classes)

# shift 1 item to right to change index to 1-BASED (start index from 1)
classes.insert(0, None)

unit_select_count = [0]
for i in range(1, n+1):
    units = classes[i].units
    last_non_conflict_index = last_non_conflict(classes, i)
    if last_non_conflict_index:
        units += unit_select_count[last_non_conflict_index]
    unit_select_count.append(max(units, unit_select_count[i-1]))

print(unit_select_count[n])