from django.contrib import admin
register = admin.site.register

# Register your models here.

from . import forms, models

register(models.Set)

@admin.register(models.Block)
class BlockAdmin(admin.ModelAdmin):

    form = forms.BlockForm

    @admin.display(description='Day')
    def admin_day(self, obj):
        return obj.day.strftime('%I:%M %p')
