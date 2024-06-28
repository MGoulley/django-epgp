from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.template import loader

import pandas as pd

from django.conf import settings

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
        return Player.objects.values('name', 'discordTag', 'isOfficier', 'isPU')
    
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
        return Character.objects.values("name", "level", "ilvl", "race", "classe", "specMain", "specAlt", "playerId__name", "id")

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
                isOfficier=form.cleaned_data.get("isOfficier"),
                isPU=form.cleaned_data.get("isPU")
            )
            player.save()
            log = EPGPLogEntry(
                target_player=player, 
                user_id=request.user, 
                type=EPGPLogEntryType.NEWPLAYER, 
                reason="Bienvenue chez les belettes", 
                ep_delta=settings.EP_NEWPLAYER, 
                gp_delta=0
            )
            log.save()
            return HttpResponseRedirect("/players")
    else:
        form = PlayerForm()

    return render(request, "player/add.html", {"form": form})

def editCharacter(request, id):
    character = Character.objects.get(id=id)
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            character.name = form.cleaned_data.get("name")
            character.level = form.cleaned_data.get("level")
            character.ilvl = form.cleaned_data.get("ilvl")
            character.race = form.cleaned_data.get("race")
            character.classe = form.cleaned_data.get("classe")
            character.specMain = form.cleaned_data.get("specMain")
            character.specAlt = form.cleaned_data.get("specAlt")
            character.save()
            return HttpResponseRedirect("/characters")
    else:  
        form = CharacterForm(instance=character)

    return render(request, "character/edit.html", {"form": form})

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

def editRaid(request, id):
    raid = Raid.objects.get(id=id)
    if request.method == "POST":
        form = RaidForm(request.POST)
        if form.is_valid():
            raid.played_at = form.cleaned_data.get("played_at")
            raid.instance = form.cleaned_data.get("instance")
            raid.warcraftLogs = form.cleaned_data.get("warcraftLogs")
            raid.commentaire = form.cleaned_data.get("commentaire")
            raid.isClosed = form.cleaned_data.get("isClosed")
            raid.save()
            raid.participants.set(form.cleaned_data.get("participants"))
            return HttpResponseRedirect("/raids")
    else:  
        form = RaidForm(instance=raid)

    return render(request, "raid/edit.html", {"form": form})

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
            ep_delta = 0
            reason = ""
            raid = form.cleaned_data.get("raid")
            nbHour = form.cleaned_data.get("nbHour")
            bossKillNM = form.cleaned_data.get("bossKillNM")
            bossKillHM = form.cleaned_data.get("bossKillHM")
            wipe = form.cleaned_data.get("wipe")

            if form.cleaned_data.get("presence") == True:
                ep_delta = ep_delta + 30
                reason = reason + "Present. "
            
            if nbHour != None:
                if nbHour > 0 and nbHour < 10:
                    ep_delta = ep_delta + (nbHour * 50)
                    reason = reason + str(nbHour) + " heures de raid. "
            
            if bossKillNM != None:
                if bossKillNM > 0 and bossKillNM < 20:
                    ep_delta = ep_delta + (bossKillNM * 30)
                    reason = reason + str(bossKillNM) + " boss tués en NM. "
            
            if bossKillHM != None:
                if bossKillHM > 0 and bossKillHM < 20:
                    ep_delta = ep_delta + (bossKillHM * 50)
                    reason = reason + str(bossKillHM) + " boss tués en HM. "
            
            if wipe != None:
                if wipe > 0 and wipe < 20:
                    ep_delta = ep_delta + (wipe * 10)
                    reason = reason + str(wipe) + " wipes sur des nouveaux boss. "
    
            characters = Raid.objects.get(id=raid.id).participants.all()
            for player_id in characters.values_list('playerId', flat=True).distinct():
                player = Player.objects.get(id=player_id)
                log = EPGPLogEntry(
                    target_player=player, 
                    user_id=request.user,
                    raid=raid,
                    type=EPGPLogEntryType.PARTICIPATE, 
                    reason=reason, 
                    ep_delta=ep_delta, 
                    gp_delta=0
                )
                log.save()
            return HttpResponseRedirect("/epgp")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GiveRaidForm()

    return render(request, "epgp/giveraid.html", {"form": form})

def sessionLootEPGP(request):
    if request.method == "POST":
        form = SelectRaidForm(request.POST)
        if form.is_valid():
            raid = form.cleaned_data.get("raid")
            return HttpResponseRedirect("/epgp/sessionloot/" + str(raid.id))
    else:
        # TODO: Retourner directement vers session loot raid si seulement un raid actif
        form = SelectRaidForm()

    return render(request, "epgp/selectraid.html", {"form": form})

def sessionLootRaidEPGP(request, id):
    # Voir si c'est pas playerId
    if request.method == "POST":
        form = GiveRaidLootForm(id, request.POST)
        if form.is_valid():
            raid = Raid.objects.get(id=id)
            characters = form.cleaned_data.get("characters").select_related().values('playerId', 'name', 'id')
            dfCharacters = pd.DataFrame.from_records(characters).rename(columns={"playerId": "id", "id": "characterId"})
            dfEPGP = pd.DataFrame.from_records(EPGPLogEntry.objects.getRankPerCharacter()).rename(columns={"target_player__id": "id", "rank": "ratio"})
            dfResult = dfCharacters.merge(dfEPGP, on='id', how='left').sort_values(by='ratio', ascending=False)
            character = dfResult['name'].iloc[0]
            player = Player.objects.get(id=dfResult['id'].iloc[0])
            loot = Loot.objects.get(inGameId=form.cleaned_data.get("loot_id"))
            reduction = 1.0
            reason = "Obtient un super loot !"
            if form.cleaned_data.get("reduction_reroll") == True:
                reduction = settings.REDUCTION_REROLL
                reason = "Obtient un super loot pour son reroll (Réduction de " + str(int(reduction * 100)) + "%)."
            if form.cleaned_data.get("reduction_spe2") == True:
                reduction = settings.REDUCTION_SPE2
                reason = "Obtient un super loot pour sa spé secondaire (Réduction de " + str(int(reduction * 100)) + "%)."
            gpValue = loot.gpValue
            
            log = EPGPLogEntry(
                target_player=player, 
                user_id=request.user, 
                type=EPGPLogEntryType.LOOT,
                reason = reason,
                raid=raid,
                loot_id=loot,
                ep_delta=0, 
                gp_delta=int(gpValue * reduction)
            )
            log.save()
            dfPrintResult = dfResult[["name", "total_ep", "total_gp", "ratio"]]
            form = GiveRaidLootForm(id)
            return render(request, "epgp/giveraidloot.html", {"form": form, "raidid": id, "saved": "yes", "modalTitle": str(character) + " remporte le loot !", "modalContent": dfPrintResult.to_html(index=False)})
    else:
        form = GiveRaidLootForm(id)

    return render(request, "epgp/giveraidloot.html", {"form": form, "raidid": id})

def applyDecay(request):
    if request.method == "POST":
        form = DecayForm(request.POST)
        if form.is_valid():
            decay=form.cleaned_data.get("decay")
            objects = EPGPLogEntry.objects.getTotalEPPerPlayer(decay)
            for player in objects:
                log = EPGPLogEntry(
                    target_player=Player.objects.get(id=player["target_player"]), 
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
                        target_player=form.cleaned_data.get("playerId"), 
                        user_id=request.user, 
                        type=EPGPLogEntryType.DOCKEP, 
                        reason=reason, 
                        ep_delta=-1 * abs(dock_value_ep), 
                        gp_delta=0
                    )
                    log.save()
                elif dock_value_gp != 0:
                    log = EPGPLogEntry(
                        target_player=form.cleaned_data.get("playerId"), 
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

def giveep(request):
    if request.method == "POST":
        form = GiveEPForm(request.POST)
        if form.is_valid():
            log = EPGPLogEntry(
                target_player=form.cleaned_data.get("playerId"), 
                user_id=request.user, 
                type=EPGPLogEntryType.OTHER, 
                reason=form.cleaned_data.get("reason"), 
                ep_delta=abs(form.cleaned_data.get("gain_ep")), 
                gp_delta=0
            )
            log.save()
            
            return HttpResponseRedirect("/epgp")
    else:
        form = GiveEPForm()

    return render(request, "epgp/giveep.html", {"form": form})

def standby(request):
    if request.method == "POST":
        form = StandbyForm(request.POST)
        if form.is_valid():
            raid = form.cleaned_data.get("raid")
            log = EPGPLogEntry(
                target_player=form.cleaned_data.get("playerId"), 
                user_id=request.user, 
                type=EPGPLogEntryType.STANDBY, 
                reason="Bench pour le raid " + raid.instance,
                raid=raid,
                ep_delta=settings.EP_STANDBY, 
                gp_delta=0
            )
            log.save()
            
            return HttpResponseRedirect("/epgp")
    else:
        form = StandbyForm()

    return render(request, "epgp/standby.html", {"form": form})

def index(request):
    if request.user.is_authenticated:
        return render(request, "index-auth.html")
    else:
        data = []
        objects = EPGPLogEntry.objects.getRankPerPlayer()
        for object in objects:
            data.append(object)

        tableranking = EPGPRankTable(data)

        tablelog = EPGPLogEntryTableLight(EPGPLogEntry.objects.all())

        return render(request, 'index.html', {'tableranking':tableranking, 'tablelog':tablelog})

def player(request, name):
    return HttpResponse("GET PLAYER INFO OF " + name)
