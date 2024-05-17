from django import forms
from .models import *
from dal import autocomplete

class PlayerForm(forms.Form):
    name = forms.CharField()
    discordTag = forms.CharField()

class CharacterForm(forms.Form):
    playerId = forms.ModelChoiceField(queryset=Player.objects.all())
    name = forms.CharField()
    level = forms.IntegerField()
    ilvl = forms.IntegerField()
    race = forms.ChoiceField(choices=Character.CharacterRace.choices,)
    classe = forms.ChoiceField(choices=Character.CharacterClass.choices,)
    specMain = forms.ChoiceField(choices=Character.CharacterSpec.choices,)
    specAlt = forms.ChoiceField(choices=Character.CharacterSpec.choices,)

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