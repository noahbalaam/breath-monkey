from django import forms
from .models import WimHofSession, BreathingRound

class WimHofSessionForm(forms.ModelForm):
    """Form for creating/editing a WimHof breathing session."""
    
    # Initial configuration
    round_count = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=3,
        label="Number of Rounds",
        help_text="How many rounds of breathing?"
    )
    
    ramp_up = forms.BooleanField(
        required=False,
        initial=True,
        label="Ramp Up Intensity",
        help_text="Gradually increase breath count in each round"
    )
    
    starting_breaths = forms.IntegerField(
        min_value=10,
        max_value=50,
        initial=30,
        label="Starting Breath Count",
        help_text="Number of breaths in the first round"
    )
    
    breath_increment = forms.IntegerField(
        min_value=0,
        max_value=20,
        initial=10,
        label="Breath Increment",
        help_text="How many extra breaths to add for each round (if ramping up)"
    )
    
    class Meta:
        model = WimHofSession
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'My WimHof Session'})
        }