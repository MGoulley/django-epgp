from django import forms
from .models import *
from dal import autocomplete

class GiveRaidForm(forms.Form):
    raid = forms.ModelChoiceField(queryset=Raid.objects.all())
    give_by = forms.ModelChoiceField(queryset=Player.objects.all())
    reason = forms.CharField()
    ep_delta = forms.IntegerField()

class GiveLootForm(forms.Form):
    target_player = forms.ModelChoiceField(queryset=Player.objects.all())
    give_by = forms.ModelChoiceField(queryset=Player.objects.all())
    class Meta:
        widgets = {
            'loot': autocomplete.ModelSelect2(url='loot-autocomplete')
        }