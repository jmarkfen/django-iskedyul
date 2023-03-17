from typing import Text
from django import forms
from crispy_forms.helper import FormHelper
from .models import Block, Set

class SetForm(forms.ModelForm):
    
    class Meta:
        model = Set
        fields = '__all__'

class BlockForm(forms.ModelForm):
    
    class Meta:
        model = Block
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.helper = FormHelper(self)
