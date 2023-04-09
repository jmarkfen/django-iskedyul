import datetime as dt

## add two time objects
def add_time(time1, time2):
    t1 = dt.datetime.strptime(f'{time1.hour}:{time1.minute}:{time1.second}', '%H:%M:%S')
    t2 = dt.datetime.strptime(f'{time2.hour}:{time2.minute}:{time2.second}', '%H:%M:%S')
    time_zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
    result =  (t1 - time_zero + t2).time()
    return result


# add minutes to a time object
def time_add_minutes(initial_time, minutes):
    t = dt.datetime.strptime(f'{initial_time.hour}:{initial_time.minute}:{initial_time.second}', '%H:%M:%S')
    m = dt.datetime.strptime(f'00:{minutes}:00', '%H:%M:%S')
    time_zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
    result =  (t - time_zero + m).time()
    return result

# blocks: queryset containing blocks (event_set.all() or event_set.filter())
# returns a dictionary with days as keys and blocks as values
def day_dict(blocks):
    time_rows = {}
    time_rows['time1'] = {}
    daycol = {}
    days = [1, 2, 3, 4, 5, 6, 7]
    for d in days:
        qs = blocks.filter(day=d)
        daycol[d] = qs[0] if len(qs) > 0 else None
    return daycol