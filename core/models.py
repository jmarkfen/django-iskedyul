import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
# Create your models here.

class Set(models.Model):

    title = models.CharField(_("title"), max_length=50)

    class Meta:
        verbose_name = _("set")
        verbose_name_plural = _("sets")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("set_list", kwargs={"pk": self.pk})

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
