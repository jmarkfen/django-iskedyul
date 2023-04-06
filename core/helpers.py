from ctypes import resize
from math import remainder
from django.db import models as dj
import datetime



class CountResult():
    def __init__(self, field: str, value, count: int, group):
        self.field = field
        self.value = value
        self.count = count
        self.group = group

    def __str__(self) -> str:
        return f'CountResult <field={self.field}, value={self.value}, count={self.count}>'

# TODO: replace all result dicts with CountResult

def count_field(queryset, field_name, field_value):
    """ count identical values in a queryset """
    # define a dictionary with the field name and the value to filter by
    filter_kwargs = {f'{field_name}': field_value, }
    # filter the queryset using the dictionary of keyword arguments
    qs =  queryset.filter(**filter_kwargs)
    # count number of records
    qs_count = qs.count()
    # define a dictionary with field name count
    annotate_kwargs = {f'{field_name}__count': dj.Value(qs_count, dj.IntegerField()), }
    # annotate the count into the queryset
    qs_annotated = qs.annotate(**annotate_kwargs)
    return qs_annotated

def countif(queryset, **filter_kwargs):
    """ return a dict containing the 'count': number of records, 'group': filtered queryset """
    # filter the queryset with the filters
    qs = queryset.filter(**filter_kwargs)
    # count number of records
    qs_count = qs.count()
    # assign values to dict
    result = {'count': qs_count, 'group': qs}
    return result

def count(queryset, field_name, field_value) -> CountResult:
    """ count identical values in a queryset """
    # define a dictionary with the field name and the value to filter by
    filter_kwargs = {f'{field_name}': field_value, }
    # get filtered queryset and count
    filtered = countif(queryset, **filter_kwargs)
    result = CountResult(field_name, field_value, filtered['count'], filtered['group'])
    return result

def count_group(queryset, field_name, field_values: list) -> list[CountResult]:
    """ return a list of querysets grouped by field_values """
    result = []
    for field_value in field_values:
        cr = count(queryset, field_name, field_value)
        result.append(cr)
    return result

# def sub_group_count(group: list, field_name, field_values: list):
#     """ count the inner queryset of a result dictionary from get_group_count """
#     for sub in group:
#         qs = get_group_count(sub['group'], field_name, field_values)
#         sub['group'] = qs
#     return group

def add_minutes(initial_time, minutes):
    """ add minutes to a time object """
    result = None
    zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    # get hours from minutes
    hrs = int(minutes / 60)
    # get extra minutes
    mins = minutes % 60
    t1 = datetime.datetime.strptime(f'{initial_time.hour}:{initial_time.minute}:{initial_time.second}', '%H:%M:%S')
    t2 = datetime.datetime.strptime(f'{hrs}:{mins}:00', '%H:%M:%S')
    result =  (t1 - zero + t2).time()
    return result

class TimetableCell():
    def __init__(self, data=None, rowspan=1, colspan=1):
        self.data = data
        self.rowspan = rowspan
        self.colspan = colspan

class TimetableDisplay():
    """ 
    2D list timetable from queryset of events
    """

    def __init__(self, queryset, weekdays: list, time_ranges):
        """ 
        weekdays - use WeekDays.choices
        """
        self.queryset = queryset
        self.weekdays = weekdays
        self.time_ranges = time_ranges
        self.day_headers = [TimetableCell(wd) for wd in weekdays]
        self.time_headers = [TimetableCell(tr) for tr in time_ranges]
        # initialize matrix with empty cells
        self.matrix = [
            [TimetableCell() for cols in range(len(weekdays))]
            for rows in range(len(time_ranges))
        ]
        
        self.table = []
        # dict of {time_range:int,}
        self.row_index = {}
        # dict of {day:int,}
        self.col_index = {}


    def exec(self):
        # 1. sort events by day then start_time
        self.queryset.order_by('day', 'start_time')
        # 2. group count by day
        day_groups = []
        for d in [n[0] for n in self.weekdays]:
            day_group = count(self.queryset, 'day', d)
            from django.db.models import Window
            from django.db.models.functions import Lag
            # 3. annotate the end_time of the previous event
            #    to the current event as previous_time
            annotated = day_group.group.annotate(previous_time=Window(expression=Lag('end_time')))
            # replace the group with the annotated queryset
            day_group.group = annotated
            # 4. if the previous_time < end_time then
            #    move event to another column
            #    increment the day header colspan
            
            day_groups.append(day_group)
            
        return day_groups
        
    def rawput_day(self, row, col, data):
        """ directly put object at matrix"""
        if self.matrix[row][col].data is None:
            # insert at location if data is None
            self.matrix[row][col].data = data
        else:
            # insert to next column if data already exists
            self.matrix[row][col + 1].data = data

def to_matrix(queryset, rows, cols):
    pass

