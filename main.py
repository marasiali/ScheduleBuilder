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

classes = []
n = int(input("Please enter the number of classes :"))
print("Enter each class details in one row with this condition :")
print("ClassName[SPACE]WeekDayAbbr[SPACE]UNITS[SPACE]StartTime(in hour)-EndTime(in hour)\n")
print("     Example :")
print("       Math SAT 3 8-10\n")

for i in range(n):
    class_name, week_day_abbr, units, class_time = input().split()
    week_day_abbr = week_day_abbr.upper()
    week_day = None
    if week_day_abbr == "SAT":
        week_day = WeekDay.SAT
    elif week_day_abbr == "SUN":
        week_day = WeekDay.SUN
    elif week_day_abbr == "MON":
        week_day = WeekDay.MON
    elif week_day_abbr == "TUE":
        week_day = WeekDay.TUE
    elif week_day_abbr == "WED":
        week_day = WeekDay.WED
    elif week_day_abbr == "THU":
        week_day = WeekDay.THU
    elif week_day_abbr == "FRI":
        week_day = WeekDay.FRI
    else:
        raise RuntimeError("Invalid weekDay !")
    units = int(units)
    start_time, end_time = list(map(int, class_time.split('-')))
    if start_time > end_time:
        raise RuntimeError("Invalid time !")
    classes.append(ClassSection(class_name, units, week_day, start_time, end_time))

classes.sort(key=lambda item: (item.week_day, item.end_time, item.start_time))

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

print('\n--------------------------------------------------------\n')
print("MAX UNIT CAN BE SELECTED :", unit_select[n][0])
for i, schedule in enumerate(unit_select[n][1]):
    print('\nSCHEDULE ({}) :'.format(i+1))
    for item in schedule:
        print(classes[item])