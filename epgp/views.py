from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.template import loader

from .filters import *
from .forms import *
from .models import *
from .tables import *


def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:

        template = loader.get_template( 'pages/error-404.html' )
        return HttpResponse(template.render(context, request))

class PlayerListView(SingleTableView):
    model = Player
    table_class = PlayerTable
    template_name = 'player/index.html'
    def get_table_data(self):
        return Player.objects.values('name', 'discordTag', 'isOfficier')
    
class LootListView(SingleTableMixin, FilterView):
    model = Loot
    table_class = LootTable
    template_name = 'loot/index.html'
    filterset_class = LootFilter
    
    def get_queryset(self):
        return Loot.objects.filter(ilvl__lte = 430)

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

def EPGPPlayerRanking(request):
    data = []
    objects = EPGPLogEntry.objects.getRankPerPlayer()
    for object in objects:
        data.append(object)

    table = EPGPRankTable(data)

    return render(request, 'epgp/ranking.html', {'table':table})

class EPGPLogEntryListView(SingleTableView):
    model = EPGPLogEntry
    table_class = EPGPLogEntryTable
    template_name = 'epgp/index.html'

def addPlayer(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = Player(
                name=form.cleaned_data.get("name"), 
                discordTag=form.cleaned_data.get("discordTag"),
                isOfficier=form.cleaned_data.get("isOfficier")
            )
            player.save()
            log = EPGPLogEntry(
                target_player_id=player, 
                user_id=request.user, 
                type=EPGPLogEntryType.NEWPLAYER, 
                reason="Bienvenue chez les belettes", 
                ep_delta=500, 
                gp_delta=0
            )
            log.save()
            return HttpResponseRedirect("/players")
    else:
        form = PlayerForm()

    return render(request, "player/add.html", {"form": form})

def addCharacter(request):
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = Character(
                playerId=form.cleaned_data.get("playerId"), 
                name=form.cleaned_data.get("name"), 
                level=form.cleaned_data.get("level"), 
                ilvl=form.cleaned_data.get("ilvl"), 
                race=form.cleaned_data.get("race"), 
                classe=form.cleaned_data.get("classe"), 
                specMain=form.cleaned_data.get("specMain"), 
                specAlt=form.cleaned_data.get("specAlt")
            )
            character.save()
            return HttpResponseRedirect("/characters")
    else:
        form = CharacterForm()

    return render(request, "character/add.html", {"form": form})

def addRaid(request):
    if request.method == "POST":
        form = RaidForm(request.POST)
        if form.is_valid():
            raid = Raid.objects.create(
                played_at=form.cleaned_data.get("played_at"), 
                instance=form.cleaned_data.get("instance"), 
                commentaire=form.cleaned_data.get("commentaire")
            )
            raid.participants.set(form.cleaned_data.get("participants"))
            return HttpResponseRedirect("/raids")
    else:
        form = RaidForm()

    return render(request, "raid/add.html", {"form": form})

def giveRaidEPGP(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = GiveRaidForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            raid_id = form.cleaned_data.get("raid").id
            reason = form.cleaned_data.get("reason")
            ep_delta = form.cleaned_data.get("ep_delta")
            characters = Raid.objects.get(id=raid_id).participants.all()
            for player_id in characters.values_list('playerId', flat=True).distinct():
                player = Player.objects.get(id=player_id)
                log = EPGPLogEntry(target_player_id=player, user_id=request.user, type=EPGPLogEntryType.PARTICIPATE, reason=reason, ep_delta=ep_delta, gp_delta=0)
                log.save()
            return HttpResponseRedirect("/epgp")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GiveRaidForm()

    return render(request, "epgp/giveraid.html", {"form": form})

def giveLootEPGP(request):
    if request.method == "POST":
        form = GiveLootForm(request.POST)
        if form.is_valid():
            character = form.cleaned_data.get("character")
            player = character.playerId
            loot = Loot.objects.get(inGameId=form.cleaned_data.get("loot_id"))
            gpValue = loot.gpValue
            log = EPGPLogEntry(
                target_player_id=player, 
                user_id=request.user, 
                type=EPGPLogEntryType.LOOT,
                loot_id=loot,
                ep_delta=0, 
                gp_delta=gpValue
            )
            log.save()
            return HttpResponseRedirect("/epgp")
    else:
        form = GiveLootForm()

    return render(request, "epgp/giveloot.html", {"form": form})

def applyDecay(request):
    if request.method == "POST":
        form = DecayForm(request.POST)
        if form.is_valid():
            decay=form.cleaned_data.get("decay")
            objects = EPGPLogEntry.objects.getTotalEPPerPlayer(decay)
            for player in objects:
                log = EPGPLogEntry(
                    target_player_id=Player.objects.get(id=player["target_player_id"]), 
                    user_id=request.user, 
                    type=EPGPLogEntryType.DECAY, 
                    reason="Decay de " + str(decay) + "%", 
                    ep_delta=-1 * player["decay"], 
                    gp_delta=0
                )
                log.save()
                
            return HttpResponseRedirect("/epgp")
    else:
        form = DecayForm()

    return render(request, "epgp/decay.html", {"form": form})

def applyDock(request):
    if request.method == "POST":
        form = DockForm(request.POST)
        if form.is_valid():
            dock_value_ep = form.cleaned_data.get("dock_value_ep")
            dock_value_gp = form.cleaned_data.get("dock_value_gp")
            reason = form.cleaned_data.get("reason")
            
            if (dock_value_ep != 0 and dock_value_gp == 0) or (dock_value_ep == 0 and dock_value_gp != 0):
                if dock_value_ep != 0:
                    log = EPGPLogEntry(
                        target_player_id=form.cleaned_data.get("playerId"), 
                        user_id=request.user, 
                        type=EPGPLogEntryType.DOCKEP, 
                        reason=reason, 
                        ep_delta=-1 * abs(dock_value_ep), 
                        gp_delta=0
                    )
                    log.save()
                elif dock_value_gp != 0:
                    log = EPGPLogEntry(
                        target_player_id=form.cleaned_data.get("playerId"), 
                        user_id=request.user, 
                        type=EPGPLogEntryType.DOCKGP, 
                        reason=reason, 
                        ep_delta=0, 
                        gp_delta=abs(dock_value_gp)
                    )
                    log.save()
                
            return HttpResponseRedirect("/epgp")
    else:
        form = DockForm()

    return render(request, "epgp/dock.html", {"form": form})

def index(request):
    return render(request, "index.html")

def player(request, name):
    return HttpResponse("GET PLAYER INFO OF " + name)
