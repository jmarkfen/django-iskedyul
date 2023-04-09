import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.db.models import Case, CharField, Count, F, Value, When
from django.db.models.functions import Trunc
from django.core.validators import MinValueValidator, MaxValueValidator
from . import helpers

# Create your models here.


# put inside block/event
class WeekDays(models.IntegerChoices):
    MONDAY = 1, _('Monday')
    TUESDAY = 2, _('Tuesday')
    WEDNESDAY = 3, _('Wednesday')
    THURSDAY = 4, _('Thursday')
    FRIDAY = 5, _('Friday')
    SATURDAY = 6, _('Saturday')
    SUNDAY = 7, _('Sunday')

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
        return reverse("table_detail", kwargs={"pk": self.pk})

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
            new_time = helpers.add_minutes(current_time, self.interval)
            time_ranges.append({'start': current_time, 'end': new_time, 'label': str(current_time) + '-' + str(new_time)})
            current_time = new_time
        return tuple(time_ranges)

    def get_matrix(self) -> dict:
        """ generate matrix data for rendering timetable """
        # get events sorted by start_time then day
        events = self.event_set.all().order_by('start_time', 'day')
        # get time ranges
        time_ranges = self.get_time_ranges()
        # map ranges start
        rows = {time_ranges[i]['start']: i for i in range(len(time_ranges))}
        # map weekday values
        day_map = {num: name for num, name in WeekDays.choices}
        # map start times and end times
        time_count = range(len(time_ranges))
        start_time_map = {time_ranges[i]['start']: i for i in time_count}
        end_time_map = {time_ranges[i]['end']: i for i in time_count}
        # create list of nones
        def nones():
            ns = []
            for i in time_count:
                ns.append(None)
            return ns
        # create dict of WeekDay

        # initialize matrix
        matrix = {
            'header_rowspans': {name: 1 for num, name in WeekDays.choices},
            day_map[1]: [nones(), ],
            day_map[2]: [nones(), ],
            day_map[3]: [nones(), ],
            day_map[4]: [nones(), ],
            day_map[5]: [nones(), ],
            day_map[6]: [nones(), ],
            day_map[7]: [nones(), ],
        }
        for e in events:
            # get key from event day
            col_index = day_map[e.day]
            subcol_index = 0
            # get key from event start time
            start_time_index = start_time_map[e.start_time]
            # get key from event end time
            end_time_index = end_time_map[e.end_time]
            row_index = rows[e.start_time]
            # TODO calculate rows from e.start_time and e.end_time
            t1 = e.start_time
            t2 = e.end_time
            # get the difference in minutes between t1 and t2 then divide by intervala
            t1_minutes = t1.hour * 60 + t1.minute
            t2_minutes = t2.hour * 60 + t2.minute
            tdiff = t2_minutes - t1_minutes
            row_count = int(tdiff / self.interval)
            # check if the current subcolumn is already occupied
            # TODO change already_occupied to a list of indices
            def none_occupied(subcol):
                """ check if any row is already occupied. Returns True if all rows are not occupied. """
                not_occupied = []
                for i in range(row_count):
                    if row_index + i < len(matrix[col_index][subcol_index]): 
                        not_occupied.append(matrix[col_index][subcol][row_index + i] is None)
                return all(not_occupied)
            
            while not none_occupied(subcol_index):
                # if current subcolumn is the last one
                if subcol_index == len(matrix[col_index]) - 1:
                    # add new subcolumn
                    matrix[col_index].append(nones())

                # change index to point at next subcolumn
                subcol_index += 1
            
            # put event in place once there is available space, also put the rowspan
            matrix[col_index][subcol_index][row_index] = {'data': e, 'rowspan': row_count}
            # set the classes for the cell
            if subcol_index > 0:
                matrix[col_index][subcol_index][row_index]['class'] = 'cell-conflict'
            else:
                matrix[col_index][subcol_index][row_index]['class'] = 'cell'
            # also set the other positions
            for i in range(1, row_count):
                if row_index + i < len(matrix[col_index][subcol_index]): 
                    matrix[col_index][subcol_index][row_index + i] = {'data': True, 'rowspan': 1}
            # also set the rowspan of the column headers
            matrix['header_rowspans'][day_map[e.day]] = len(matrix[col_index])

        return matrix

                
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
