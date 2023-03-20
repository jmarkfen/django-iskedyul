import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.db.models import Case, CharField, Count, F, Value, When
from django.db.models.functions import Trunc
# from .oop import time_add_minutes

def time_add_minutes(initial_time, minutes):
    """ add minutes to a time object """
    t = datetime.datetime.strptime(f'{initial_time.hour}:{initial_time.minute}:{initial_time.second}', '%H:%M:%S')
    m = datetime.datetime.strptime(f'00:{minutes}:00', '%H:%M:%S')
    time_zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    result =  (t - time_zero + m).time()
    return result


# Create your models here.

class Set(models.Model):

    title = models.CharField(_("title"), max_length=50)
    # notes
    # minute_interval

    class Meta:
        verbose_name = _("set")
        verbose_name_plural = _("sets")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("set_detail", kwargs={"pk": self.pk})

    def get_time_ranges(self):
        """ generate time ranges based on interval """
        # TODO: replace with interval as a Set field
        interval = 30
        # set start time
        start_time = datetime.time(00,00)
        # set end time (last row will be +30 min)
        end_time = datetime.time(20, 00)
        # generate time_ranges
        time_ranges = []
        current_time = start_time
        while current_time <= end_time:
            new_time = time_add_minutes(current_time, interval)
            time_ranges.append((current_time, new_time, str(current_time) + '-' + str(new_time)))
            current_time = new_time
        return time_ranges

    def get_matrix(self):
        """ returns a 2x2 matrix where the rows are start times and days are columns 
            usage: Set.objects.get(pk=id).get_matrix()
        """
        # step 1: group into start times
        # step 2: for each group, sort elements by day
        # step 3: mark conflicts by checking each group for events in the same day
        # step 4: create matrixq
        #         for conflicts, insert a new column to put the second item
        #         also insert columns on the same index on other rows
        # generate time_ranges
        time_ranges = self.get_time_ranges()
        # create queryset with events sorted by start_time then day
        qs = self.block_set.all().order_by('start_time', 'day')
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
        ).values('time_range', 'text', 'day', 'start_time', 'end_time')
        # annotate queryset with conflict

        # TODO: test blocks with same day and time range
        # return queryset
        return qs
        
    def get_rows(self):
        """ get rows sorted by time ranges """
        labels = [t[2] for t in self.get_time_ranges()]
        matrix = self.get_matrix()
        rows = []
        for label in labels:
            # get only records in label time range
            m = matrix.filter(time_range=label)
            # count number of records
            m_count = m.count()
            # annotate the count to the records
            m_annot = m.annotate(range_count=Value(label, models.CharField()))
            # append to label and the queryset to rows
            rows.append((label, m_annot))
        return rows

class DayDefaults(models.TextChoices):
    MONDAY = 'Monday'
    TUESDAY  = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'


# put inside block/event
class WeekDays(models.IntegerChoices):
    MONDAY = 1, _('Monday')
    TUESDAY = 2, _('Tuesday')
    WEDNESDAY = 3, _('Wednesday')
    THURSDAY = 4, _('Thursday')
    FRIDAY = 5, _('Friday')
    SATURDAY = 6, _('Saturday')
    SUNDAY = 7, _('Sunday')

    __empty__ = _('(Unknown)')


DEFAULT_DAYS = ('Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

DEFAULT_TIME = ('07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', 
                '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', 
                '17:00', '17:30', '18:00', '19:30', '20:00', '20:30')
                

class Block(models.Model):

    set = models.ForeignKey("core.Set", on_delete=models.CASCADE)
    text = models.CharField(_("text"), max_length=50)
    start_time = models.TimeField(default=datetime.time(00, 00), auto_now=False, auto_now_add=False)
    end_time = models.TimeField(default=datetime.time(00, 00), auto_now=False, auto_now_add=False)
    day = models.CharField(max_length=50, choices=[
        ('Mon', _('Monday')),
        ('Tue', _('Tuesday')),
        ('Wed', _('Wednesday')),
        ('Thu', _('Thursday')),
        ('Fri', _('Friday')),
        ('Sat', _('Saturday')),
        ('Sun', _('Sunday')),
    ])

    class Meta:
        verbose_name = _("block")
        verbose_name_plural = _("blocks")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("block_detail", kwargs={"pk": self.pk})

