from django import forms
from .models import *

class EPGPLogEntryForm(forms.Form):
    target_player_id = forms.ModelChoiceField(queryset=Player.objects.all())
    source_player_id = forms.ModelChoiceField(queryset=Player.objects.all())
    type = forms.ChoiceField(choices=EPGPLogEntry.EPGPLogEntryType.choices)
