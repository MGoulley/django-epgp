from django import forms
from .models import *
from django.core.exceptions import ValidationError

def validate_loot_exists(value):
    incident = Loot.objects.filter(inGameId=value)
    if not incident: # check if any object exists
        raise ValidationError("L'item n'existe pas") 

class PlayerForm(forms.Form):
    name = forms.CharField(label="Nom du joueur")
    discordTag = forms.CharField(label="Tag discord")
    isOfficier = forms.BooleanField(label="Est un officier", required=False, initial=False,)

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DecayForm(forms.Form):
    decay = forms.FloatField(label="Valeur du decay (en pourcentage)")

    def __init__(self, *args, **kwargs):
        super(DecayForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DockForm(forms.Form):
    playerId = forms.ModelChoiceField(label="Joueur", error_messages={"required": "Choisir un joueur"}, queryset=Player.objects.all())
    dock_value_ep = forms.IntegerField(label="Malus en EP", required=False, initial=0)
    dock_value_gp = forms.IntegerField(label="Malus en GP", required=False, initial=0)
    reason = forms.CharField(label="Raison", required=True)

    def __init__(self, *args, **kwargs):
        super(DockForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class GiveEPForm(forms.Form):
    playerId = forms.ModelChoiceField(label="Joueur", error_messages={"required": "Choisir un joueur"}, queryset=Player.objects.all())
    gain_ep = forms.IntegerField(label="Bonus en EP", required=True)
    reason = forms.CharField(label="Raison", required=True)

    def __init__(self, *args, **kwargs):
        super(GiveEPForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class StandbyForm(forms.Form):
    playerId = forms.ModelChoiceField(label="Joueur", error_messages={"required": "Choisir un joueur"}, queryset=Player.objects.all())
    raid = forms.ModelChoiceField(label="Raid", error_messages={"required": "Choisir un raid"}, queryset=Raid.objects.all().order_by("-played_at"))

    def __init__(self, *args, **kwargs):
        super(StandbyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CharacterForm(forms.Form):
    playerId = forms.ModelChoiceField(label="Joueur", error_messages={"required": "Choisir un joueur"}, queryset=Player.objects.all())
    name = forms.CharField(label="Nom du personnage")
    level = forms.IntegerField(label="Niveau")
    ilvl = forms.IntegerField(label="Niveau d'item")
    race = forms.ChoiceField(label="Race", choices=Character.CharacterRace.choices,)
    classe = forms.ChoiceField(label="Classe", choices=Character.CharacterClass.choices,)
    specMain = forms.ChoiceField(label="Spé principale", choices=Character.CharacterSpec.choices,)
    specAlt = forms.ChoiceField(label="Spé secondaire", choices=Character.CharacterSpec.choices,)

    def __init__(self, *args, **kwargs):
        super(CharacterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RaidForm(forms.Form):
    played_at = forms.DateField(label="Débuté le", initial=datetime.now)
    instance = forms.ChoiceField(label="Instance", choices=Raid.RaidInstance.choices,)
    participants = forms.ModelMultipleChoiceField(label="Participants",
        queryset=Character.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    commentaire = forms.CharField(label="Commentaire")

    def __init__(self, *args, **kwargs):
        super(RaidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class GiveRaidForm(forms.Form):
    raid = forms.ModelChoiceField(label="Raid", queryset=Raid.objects.all())
    reason = forms.CharField(label="Raison")
    ep_delta = forms.IntegerField(label="Gain de EP")

    def __init__(self, *args, **kwargs):
        super(GiveRaidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class GiveLootForm(forms.Form):
    character = forms.ModelChoiceField(label="Nom du personnage qui recoit un item", queryset=Character.objects.all())
    loot_id = forms.IntegerField(label="Identifiant de l'item", validators=[validate_loot_exists])

    error_css_class = 'alert alert-warning'
    
    def __init__(self, *args, **kwargs):
        super(GiveLootForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'