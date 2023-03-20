import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.db.models import Case, CharField, Count, F, Value, When
from django.db.models.functions import Trunc
from django.core.validators import MinValueValidator, MaxValueValidator
from . import helpers as hp
# from .oop import time_add_minutes

def time_add_minutes(initial_time, minutes):
    """ add minutes to a time object """
    t = datetime.datetime.strptime(f'{initial_time.hour}:{initial_time.minute}:{initial_time.second}', '%H:%M:%S')
    m = datetime.datetime.strptime(f'00:{minutes}:00', '%H:%M:%S')
    time_zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    result =  (t - time_zero + m).time()
    return result


# Create your models here.

class Timetable(models.Model):

    title = models.CharField(max_length=50)
    notes = models.CharField(default=None, max_length=240)
    interval = models.PositiveIntegerField(default=30, validators=[MinValueValidator(0), MaxValueValidator(59)])

    # class Meta:
    #     verbose_name = _("timetable")
    #     verbose_name_plural = _("timetables")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("set_detail", kwargs={"pk": self.pk})

    def get_time_ranges(self):
        """ generate time ranges based on interval """
        # set start time
        # TODO: find event with fist start_time and use it
        start_time = datetime.time(00,00)
        # set end time (last row will be +30 min)
        # TODO: find the event with last end_time and use it
        end_time = datetime.time(20, 00)
        # generate time_ranges
        time_ranges = []
        current_time = start_time
        while current_time <= end_time:
            new_time = time_add_minutes(current_time, self.interval)
            time_ranges.append((current_time, new_time, str(current_time) + '-' + str(new_time)))
            current_time = new_time
        return time_ranges

    def by_time_range(self):
        """ returns a queryset annotated with the time range """
        # step 1: group into start times
        # step 2: for each group, sort elements by day
        # step 3: mark conflicts by checking each group for events in the same day
        # step 4: create matrixq
        #         for conflicts, insert a new column to put the second item
        #         also insert columns on the same index on other rows
        # generate time_ranges
        time_ranges = self.get_time_ranges()
        # create queryset with events sorted by start_time then day
        qs = self.event_set.all().order_by('start_time', 'day')
        # create when clauses for annotating time ranges
        whens = []
        for t1, t2, label in time_ranges:
            # when condition then label
            # TODO: format time label
            whens.append(When(start_time__gte=t1, start_time__lt=t2, then=Value(label)))
        # annotate queryset with time ranges
        qs = qs.annotate(
            time_range=Case(
                *whens,
                default=Value('other'),
                output_field=models.CharField(),
            )
        ).values('timetable_id', 'id', 'text', 'day', 'start_time', 'end_time', 'time_range')
        # annotate queryset with conflict

        # TODO: test blocks with same day and time range
        # return queryset
        return qs
        
    def get_rows(self):
        """ get rows sorted by time ranges """
        labels = [t[2] for t in self.get_time_ranges()]
        matrix = self.by_time_range()
        rows = []
        for label in labels:
            # get only records in the time range
            m = matrix.filter(time_range=label)
            # count records with identical time_ranges
            m_annot = hp.count(m, 'time_range', label)
            
            rows.append({'label': label, 'queryset': m_annot})
        return rows

    def get_table(self):
        """ generate table data for html template """
        qs = self.by_time_range
        
        pass

# put inside block/event
class WeekDays(models.IntegerChoices):
    MONDAY = 1, _('Monday')
    TUESDAY = 2, _('Tuesday')
    WEDNESDAY = 3, _('Wednesday')
    THURSDAY = 4, _('Thursday')
    FRIDAY = 5, _('Friday')
    SATURDAY = 6, _('Saturday')
    SUNDAY = 7, _('Sunday')
                
class Event(models.Model):

    timetable = models.ForeignKey("core.Timetable", on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    start_time = models.TimeField(default=datetime.time(00, 00), auto_now=False, auto_now_add=False)
    end_time = models.TimeField(default=datetime.time(00, 00), auto_now=False, auto_now_add=False)
    day = models.PositiveIntegerField(choices=WeekDays.choices)

    # class Meta:
    #     verbose_name = _("event")
    #     verbose_name_plural = _("events")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("block_detail", kwargs={"pk": self.pk})

