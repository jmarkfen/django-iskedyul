from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
# Timeblock - contains a day, start_time, content, and end_time
# Timeset - contains many timeblocks

    
class Timeblock(models.Model):

    DAYS_OF_WEEK = [
        ('Mon', _('Monday')),
        ('Tue', _('Tuesday')),
        ('Wed', _('Wednesday')),
        ('Thu', _('Thursday')),
        ('Fri', _('Friday')),
        ('Sat', _('Saturday')),
        ('Sun', _('Sunday')),
    ]
    day = models.CharField(max_length=50, choices=DAYS_OF_WEEK)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    content = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("timeblock")
        verbose_name_plural = _("timeblocks")

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("timeblock_detail", kwargs={"pk": self.pk})


class Timeset(models.Model):

    title = models.CharField(max_length=50)
    timeblocks = models.ManyToManyField(Timeblock)

    class Meta:
        verbose_name = _("timeset")
        verbose_name_plural = _("timesets")

    def __str__(self):
        return 'self.name'

    def get_absolute_url(self):
        return reverse("timeset_detail", kwargs={"pk": self.pk})
