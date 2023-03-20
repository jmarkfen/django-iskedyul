from typing import Text
from django import forms
from django.utils.translation import gettext as _
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from .models import Event, Timetable

class SetForm(forms.ModelForm):
    
    class Meta:
        model = Timetable
        fields = '__all__'


class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = '__all__'


# class EventForm(forms.Form):

#     text = forms.CharField(
#         max_length = 50, 
#         required = True,
#     )
#     day = forms.ChoiceField(
#         choices = (
#         ('Mon', _('Monday')),
#         ('Tue', _('Tuesday')),
#         ('Wed', _('Wednesday')),
#         ('Thu', _('Thursday')),
#         ('Fri', _('Friday')),
#         ('Sat', _('Saturday')),
#         ('Sun', _('Sunday')),
#         ),
#         required = True,
#     )
#     start_time = forms.TimeField(

#         required = True,
#     )
#     end_time = forms.TimeField(

#         required = True,
#     )

#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     self.helper = FormHelper(self)
#     #     self.helper.form_id = 'id-exampleForm'
#     #     self.helper.form_class = 'blueForms'
#     #     self.helper.form_method = 'post'
#     #     self.helper.form_action = 'submit_survey'
#     #     self.helper.add_input(Submit('submit', 'Submit'))
#     #     self.helper.form_class = 'form-horizontal'
#     #     self.helper.label_class = 'col-lg-2'
#     #     self.helper.field_class = 'col-lg-8'
#     #     self.helper.layout = Layout(
#     #             'email',
#     #             'password',
#     #             'remember_me',
#     #             StrictButton('Sign in', css_class='btn-default'),
#     #     )



