from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Timetable(models.Model):

    

    class Meta:
        verbose_name = _("Timetable")
        verbose_name_plural = _("Timetables")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Timetable_detail", kwargs={"pk": self.pk})


class Event(models.Model):

    

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Event_detail", kwargs={"pk": self.pk})
