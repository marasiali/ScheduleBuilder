from enum import IntEnum
class WeekDay(IntEnum):
    SAT = 0
    SUN = 1
    MON = 2
    TUE = 3
    WED = 4
    THU = 5
    FRI = 6

class ClassSection:
    def __init__(self, name:str, units:int, week_day:WeekDay, start_time:int, end_time:int):
        self.name = name
        self.units = units
        self.week_day = week_day
        self.start_time = start_time
        self.end_time= end_time

    def get_day(self):
        day_dict = { 
            0 : 'Saturday',
            1 : 'Sunday',
            2 : 'Monday',
            3 : 'Tuesday',
            4 : 'Wednesday',
            5 : 'Thursday',
            6 : 'Friday'
        }
        return day_dict.get(self.week_day, 'INVALID DAY')
    def __str__(self):
        return "{} ({} units) / {} : {}-{}".format(self.name, self.units, self.get_day(), self.start_time, self.end_time)


def last_non_conflict(class_list:list, item_index:int) -> int:
    for i in range(item_index-1, 0, -1):
        if class_list[i].end_time <= class_list[item_index].start_time \
            or class_list[i].week_day != class_list[item_index].week_day:
            return i

classes = [
    ClassSection('G', 2, WeekDay.SAT, 10, 12),
    ClassSection('A', 3, WeekDay.SAT, 8, 10),
    ClassSection('I', 3, WeekDay.SAT, 14, 16),
    ClassSection('C', 2, WeekDay.SAT, 8, 9),
    ClassSection('F', 3, WeekDay.SAT, 11, 13),
    ClassSection('B', 3, WeekDay.SAT, 9, 11),
    ClassSection('E', 3, WeekDay.SAT, 10, 12),
    ClassSection('H', 2, WeekDay.SAT, 11, 12),
    ClassSection('D', 2, WeekDay.SAT, 10, 11)
]

classes.sort(key=lambda item: (item.week_day, item.end_time, item.start_time))
n = len(classes)

# shift 1 item to right to change index to 1-BASED (start index from 1)
classes.insert(0, None)


# each item in format (unit_select_count, selected_units_indexes)
unit_select = [ [0, []] ]
for i in range(1, n+1):
    units = classes[i].units
    units_paths = [ [i] ]
    last_non_conflict_index = last_non_conflict(classes, i)
    if last_non_conflict_index:
        units += unit_select[last_non_conflict_index][0]
        units_paths = unit_select[last_non_conflict_index][1]
        if len(units_paths) > 0:
            units_paths = list(map( lambda item: item + [i], units_paths))
        else:
            units_paths.append([i])
    if units > unit_select[i-1][0]:
        unit_select.append([units, units_paths])
    elif units == unit_select[i-1][0]:
        unit_select.append([ units, units_paths + unit_select[i-1][1] ])
    else:
        # [:] used to copy list
        unit_select.append(unit_select[i-1][:])

print("MAX UNIT CAN BE SELECTED :", unit_select[n][0])
for i, schedule in enumerate(unit_select[n][1]):
    print('\nSCHEDULE ({}) :'.format(i+1))
    for item in schedule:
        print(classes[item])