from django import forms
from . import models as m
class TimeblockForm(forms.ModelForm):
    
    class Meta:
        model = m.Timeblock
        fields = '__all__'


class TimesetForm(forms.ModelForm):
    
    class Meta:
        model = m.Timeset
        fields = '__all__'

