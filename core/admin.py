from django.contrib import admin
register = admin.site.register

# Register your models here.
from . import models as m
from . import forms as f

@admin.register(m.Timeblock)
class TimeblockAdmin(admin.ModelAdmin):

    form = f.TimeblockForm

    @admin.display(description='Day')
    def admin_day(self, obj):
        return obj.day.strftime('%I:%M %p')


register(m.Timeset)