from django import forms
from .models import *
from dal import autocomplete

class PlayerForm(forms.Form):
    name = forms.CharField()
    discordTag = forms.CharField()
    isOfficier = forms.BooleanField(required=False, initial=False,)

class CharacterForm(forms.Form):
    playerId = forms.ModelChoiceField(queryset=Player.objects.all())
    name = forms.CharField()
    level = forms.IntegerField()
    ilvl = forms.IntegerField()
    race = forms.ChoiceField(choices=Character.CharacterRace.choices,)
    classe = forms.ChoiceField(choices=Character.CharacterClass.choices,)
    specMain = forms.ChoiceField(choices=Character.CharacterSpec.choices,)
    specAlt = forms.ChoiceField(choices=Character.CharacterSpec.choices,)

class RaidForm(forms.Form):
    played_at = forms.DateField(initial=datetime.now)
    instance = forms.ChoiceField(choices=Raid.RaidInstance.choices,)
    participants = forms.ModelMultipleChoiceField(
        queryset=Character.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    commentaire = forms.CharField()

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