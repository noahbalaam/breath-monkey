from django import forms
from .models import BreathingTechnique

class BreathingTechniqueForm(forms.ModelForm):
    in_time = forms.IntegerField(required=True, min_value=0)
    in_hold_time = forms.IntegerField(required=False, min_value=0)
    out_time = forms.IntegerField(required=True, min_value=0)
    out_hold_time= forms.IntegerField(required=False, min_value=0)
    
    class Meta:
        model = BreathingTechnique
        fields = ['name', 'in_time', 'in_hold_time', 'out_time','out_hold_time']