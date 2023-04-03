from django.test import TestCase

# Create your tests here.

def test1():
    from core import models, helpers
    tb = models.Timetable.objects.get(pk=1)
    d = helpers.TimetableDisplay(tb.event_set.all(), models.WeekDays.choices, tb.get_time_ranges())
    x = d.exec()
    print(x[0])
    print(x[0].group)
    print(x[0].group[0])
    print(x[0].group.values())

def test2():
    from django.db.models import Window, F
    from django.db.models.functions import Lag
    from .models import Event
    window = Window(order_by=F('start_time'))
    events = Event.objects.annotate(previous_time=Lag('end_time', default=None, window=window))
    for event in events:
        print(f"Event {event.id}: start={event.start_time}, end={event.end_time}, previous={event.previous_time}")


def test3():
    from django.db.models import Window, F
    from django.db.models.functions import Lag
    from .models import Event
    qs = Event.objects.annotate(
        previous_time=Window(
            expression=Lag('end_time', default=0),
            partition_by=['id', 'start_time', 'end_time'],
            order_by=F('start_time').asc(),
        )
    ).values('id', 'start_time', 'end_time', 'previous_time')
    return qs


def test4():
    """H: each event is annotated with the end_time of the previous event """
    from django.db.models import Window
    from django.db.models.functions import Lag
    from .models import Event
    result = Event.objects.annotate(prev_time=Window(expression=Lag('end_time')))
    return result

def test_TimetableDisplay():
    from .models import Timetable, WeekDays
    from .helpers import TimetableDisplay
    tt = Timetable.objects.get(pk=1)
    tb = TimetableDisplay(tt.event_set.all(), WeekDays.choices, tt.get_time_ranges())
    return tb.exec()

def test_Timetable_get_matrix():
    from .models import Timetable
    tt = Timetable.objects.get(pk=1)
    matrix = tt.get_matrix()
    print(matrix)
    print(tt.event_set.all()[0].day)