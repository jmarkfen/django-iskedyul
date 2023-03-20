from django.db import models as dj

def count(queryset, field_name, field_value):
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

def group_count(queryset, field_name, field_values: list):
    """ count multiple identical values """
    qs_groups = []
    for field_value in field_values:
        # annotate number of records with field_value
        qs = count(queryset, field_name, field_value)
        # append a tuple with field_value and the annotated queryset
        qs_groups.append({f'{field_name}': field_value, 'queryset': qs})
    return qs_groups

def get_count(queryset, field_name, field_value):
    """ count identical values in a queryset """
    # define a dictionary with the field name and the value to filter by
    filter_kwargs = {f'{field_name}': field_value, }
    # filter the queryset using the dictionary of keyword arguments
    qs =  queryset.filter(**filter_kwargs)
    # count number of records
    qs_count = qs.count()
    result = {'field': field_name, 'value': field_value, 'count': qs_count, 'queryset': qs}
    return result

def get_group_count(queryset, field_name, field_values: list):
    """ count multiple identical values """
    result = []
    for field_value in field_values:
        qs = get_count(queryset, field_name, field_value)
        result.append(qs)
    return result

# def sub_group_count(group: list, field_name, field_values: list):
#     """ count the inner queryset of a result dictionary from get_group_count """
#     for sub in group:
#         qs = get_group_count(sub['queryset'], field_name, field_values)
#         sub['queryset'] = qs
#     return group
