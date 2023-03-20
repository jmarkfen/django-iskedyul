from django.contrib import admin
register = admin.site.register

# Register your models here.

from . import forms, models

register(models.Timetable)

@admin.register(models.Event)
class BlockAdmin(admin.ModelAdmin):

    form = forms.EventForm

    @admin.display(description='Day')
    def admin_day(self, obj):
        return obj.day.strftime('%I:%M %p')
