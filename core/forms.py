from django import forms
from .models import Set, Block

class SetForm(forms.ModelForm):
    
    class Meta:
        model = Set
        fields = '__all__'

class BlockForm(forms.ModelForm):
    
    class Meta:
        model = Block
        fields = '__all__'

