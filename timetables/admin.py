from django.contrib import admin
from .models import Timetable, Event
from django.utils import timezone
timezone.activate("Asia/Manila")


# Register your models here.

admin.site.register(Timetable)
admin.site.register(Event)