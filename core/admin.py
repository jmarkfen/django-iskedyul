from django.contrib import admin
from django import forms
from . import models
register = admin.site.register

# Register your models here.

register(models.Timetable)

class EventForm(forms.ModelForm):
    
    class Meta:
        model = models.Event
        fields = '__all__'

@admin.register(models.Event)
class BlockAdmin(admin.ModelAdmin):

    form = EventForm

    @admin.display(description='Day')
    def admin_day(self, obj):
        return obj.day.strftime('%I:%M %p')
