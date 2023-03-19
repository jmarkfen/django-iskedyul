from re import DOTALL
from .models import Block
import datetime as dt

t1 = dt.datetime.strptime('12:00:00', '%H:%M:%S')
t2 = dt.datetime.strptime('02:00:00', '%H:%M:%S')
time_zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
print((t1 - time_zero + t2).time())



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

DEFAULT_DAYS = ('Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
DEFAULT_D = ('Mon', 'Tue','Wed', 'Thu', 'Fri', 'Sat', 'Sun')

DEFAULT_TIME = ('07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', 
                '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', 
                '17:00', '17:30', '18:00', '19:30', '20:00', '20:30')

class Cell:

    def __init__(self, text='', tags=[]):
        self.text = text
        self.tags = tags

# blocks: queryset containing blocks (block_set.all() or block_set.filter())
# returns a dictionary with days as keys and blocks as values
def day_dict(blocks):
    time_rows = {}
    time_rows['time1'] = {}
    daycol = {}
    for d in DEFAULT_D:
        qs = blocks.filter(day=d)
        daycol[d] = qs[0] if len(qs) > 0 else None
    return daycol


def block_row(blocks, start):
    row = {}
    for d in DEFAULT_D:
        qs = blocks.filter(day=d, start_time=start)
        # cell.tag = conflict
        pass
    pass

