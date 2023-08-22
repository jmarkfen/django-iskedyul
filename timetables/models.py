from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.



class Timetable(models.Model):

    # owner
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # title
    title = models.CharField(max_length=255)
    # upper limit
    # lower limit
    # intervals
    INTERVALS = {
        10: '10 minutes',
        20: '20 minutes',
        30: '30 minutes',
        60: '60 minutes',
    }
    # interval
    interval = models.PositiveIntegerField(default=30, validators=[MinValueValidator(0), MaxValueValidator(60)], choices=INTERVALS.items())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Timetable_detail", kwargs={"pk": self.pk})


class Event(models.Model):

    # timetable
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    # start time
    start_time = models.TimeField()
    # end time
    end_time = models.TimeField()
    # content
    content = models.TextField()

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("Event_detail", kwargs={"pk": self.pk})
