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
    isPU = forms.BooleanField(label="Est un Pick Up", required=False, initial=False,)

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
    raid = forms.ModelChoiceField(label="Raid", error_messages={"required": "Choisir un raid"}, queryset=Raid.objects.filter(isClosed=False).order_by("-played_at"))

    def __init__(self, *args, **kwargs):
        super(StandbyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CharacterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'forms/widgets/custom.html'
    characters=dict ((o['id'], o) for o in Character.objects.all().select_related().values('playerId', 'name', 'id', 'classe'))

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        ctx = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        ctx['color'] = self.characters[value]["classe"].lower()
        return ctx
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context

class RaidForm(forms.ModelForm):
    played_at = forms.DateField(label="Débuté le", initial=datetime.now)
    instance = forms.ChoiceField(label="Instance", choices=Raid.RaidInstance.choices,)
    participants = forms.ModelMultipleChoiceField(
        label="Participants",
        queryset=Character.objects.all().order_by("name"),
        widget=CustomCheckboxSelectMultiple()
    )
    warcraftLogs = forms.URLField(max_length=200, label='URL Warcraft Logs', required=False)
    commentaire = forms.CharField(label="Commentaire", required=False)
    isClosed = forms.BooleanField(label="Terminé", required=False, initial=False)

    class Meta:
        model = Raid
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RaidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class GiveRaidForm(forms.Form):
    raid = forms.ModelChoiceField(label="Raid", queryset=Raid.objects.filter(isClosed=False))
    presence = forms.BooleanField(label="Présence à l'heure (30 EP)", required=False, initial=False)
    nbHour = forms.IntegerField(label="Nombre d'heures de raid (50 EP par heure)", required=False)
    bossKillNM = forms.IntegerField(label="Nombre de boss tués en NM (30 EP par boss)", required=False)
    bossKillHM = forms.IntegerField(label="Nombre de boss tués en HM (50 EP par boss)", required=False)
    wipe = forms.IntegerField(label="Wipe sur un nouveau boss (10 EP par boss)", required=False)

    def __init__(self, *args, **kwargs):
        super(GiveRaidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SelectRaidForm(forms.Form):
    raid = forms.ModelChoiceField(label="Raid", queryset=Raid.objects.filter(isClosed=False).order_by("-played_at"), initial=0)
    
    def __init__(self, *args, **kwargs):
        super(SelectRaidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class GiveRaidLootForm(forms.Form):
    loot_id = forms.IntegerField(label="Identifiant de l'item", validators=[validate_loot_exists])
    reduction_spe2 = forms.BooleanField(label="Reduction spé 2", required=False, initial=False)
    reduction_reroll = forms.BooleanField(label="Reduction reroll", required=False, initial=False)

    error_css_class = 'alert alert-warning'
    
    def __init__(self, idRaid, *args, **kwargs):
        super(GiveRaidLootForm, self).__init__(*args, **kwargs)
        self.fields['characters'] = forms.ModelMultipleChoiceField(
            label="Nom des personnages qui veulent l'item",
            queryset=Raid.objects.get(id=idRaid).participants.order_by("name"),
            widget=CustomCheckboxSelectMultiple()
        )
        self.fields['loot_id'].widget.attrs['oninput'] = "changeWowHeadLink();"
        self.fields['loot_id'].widget.attrs['oninput'] = "changeWowHeadLink();"
        self.fields['loot_id'].widget.attrs['class'] = "form-control"
        self.fields['reduction_spe2'].widget.attrs['class'] = "col-lg-6"
        self.fields['reduction_reroll'].widget.attrs['class'] = "col-lg-6"

class ReattributeForm(forms.ModelForm):
    class Meta:
        model = EPGPLogEntry
        fields = ['target_player']

    def __init__(self, *args, **kwargs):
        super(ReattributeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
