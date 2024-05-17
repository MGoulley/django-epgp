from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from dal import autocomplete

from .filters import *
from .forms import *
from .models import *
from .tables import *

class PlayerListView(SingleTableView):
    model = Player
    table_class = PlayerTable
    template_name = 'player/index.html'
    def get_table_data(self):
        return Player.objects.values('name', 'discordTag', 'owner__name')
    
class LootListView(SingleTableView, FilterView):
    model = Loot
    table_class = LootTable
    template_name = 'loot/index.html'
    filterset_class = LootFilter
    
    def get_table_data(self):
        return Loot.objects.filter(ilvl__lte = 430)

class LootAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Loot.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class RaidListView(SingleTableView):
    model = Raid
    table_class = RaidTable
    template_name = 'raid/index.html'

class CharacterListView(SingleTableView):
    model = Character
    table_class = CharacterTable
    template_name = 'character/index.html'
    def get_table_data(self):
        return Character.objects.values("name", "level", "ilvl", "race", "classe", "specMain", "specAlt", "playerId__name")

class EPGPLogEntryListView(SingleTableView):
    model = EPGPLogEntry
    table_class = EPGPLogEntryTable
    template_name = 'epgp/index.html'

def addPlayer(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            discordTag = form.cleaned_data.get("discordTag")
            player = Player(name=name, discordTag=discordTag)
            player.save()
            return HttpResponseRedirect("/players")
    else:
        form = PlayerForm()

    return render(request, "player/add.html", {"form": form})

def addCharacter(request):
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            playerId = form.cleaned_data.get("playerId")
            name = form.cleaned_data.get("name")
            level = form.cleaned_data.get("level")
            ilvl = form.cleaned_data.get("ilvl")
            race = form.cleaned_data.get("race")
            classe = form.cleaned_data.get("classe")
            specMain = form.cleaned_data.get("specMain")
            specAlt = form.cleaned_data.get("specAlt")
            character = Character(playerId=playerId, name=name, level=level, ilvl=ilvl, race=race, classe=classe, specMain=specMain, specAlt=specAlt)
            character.save()
            return HttpResponseRedirect("/characters")
    else:
        form = CharacterForm()

    return render(request, "character/add.html", {"form": form})

def giveRaidEPGP(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = GiveRaidForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            from_user = form.cleaned_data.get("give_by")
            raid_id = form.cleaned_data.get("raid").id
            reason = form.cleaned_data.get("reason")
            ep_delta = form.cleaned_data.get("ep_delta")
            characters = Raid.objects.get(id=raid_id).participants.all()
            for player_id in characters.values_list('playerId', flat=True).distinct():
                player = Player.objects.get(id=player_id)
                log = EPGPLogEntry(target_player_id=player, source_player_id=from_user, type=EPGPLogEntryType.PARTICIPATE, reason=reason, ep_delta=ep_delta, gp_delta=0)
                log.save()
            return HttpResponseRedirect("/epgp")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GiveRaidForm()

    return render(request, "epgp/giveraid.html", {"form": form})

def giveLootEPGP(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = GiveLootForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            from_user = form.cleaned_data.get("give_by")
            raid_id = form.cleaned_data.get("raid").id
            reason = form.cleaned_data.get("reason")
            ep_delta = form.cleaned_data.get("ep_delta")
            characters = Raid.objects.get(id=raid_id).participants.all()
            for player_id in characters.values_list('playerId', flat=True).distinct():
                player = Player.objects.get(id=player_id)
                log = EPGPLogEntry(target_player_id=player, source_player_id=from_user, type=EPGPLogEntryType.PARTICIPATE, reason=reason, ep_delta=ep_delta, gp_delta=0)
                log.save()
            return HttpResponseRedirect("/epgp")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GiveLootForm()

    return render(request, "epgp/giveloot.html", {"form": form})

def index(request):
    return render(request, "index.html")

def player(request, name):
    return HttpResponse("GET PLAYER INFO OF " + name)
