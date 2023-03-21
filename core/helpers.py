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