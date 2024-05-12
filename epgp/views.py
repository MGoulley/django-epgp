from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_tables2 import SingleTableView
from django_filters.views import FilterView

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

def lootListView(request):
    queryset = Loot.objects.filter(ilvl__lte = 430)

    f = LootFilter(request.GET, queryset=queryset)
    table = LootTable(data=f.qs)
    return render(request, 'loot/index.html', {'filter': f, 'table': table})

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

def giveEPGP(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = EPGPLogEntryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EPGPLogEntryForm()

    return render(request, "/epgp/give.html", {"form": form})

def index(request):
    return HttpResponse("PAGE D'ACCUEIL")

def player(request, name):
    return HttpResponse("GET PLAYER INFO OF " + name)
