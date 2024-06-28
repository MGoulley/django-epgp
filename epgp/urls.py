from django.urls import re_path, path
from django.contrib.auth.decorators import login_required

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.index, name="home"),
    re_path(r'^.*\.html', views.pages, name='pages'),
    path("players", login_required(PlayerListView.as_view())),
    path("player/add", login_required(views.addPlayer), name="newplayer"),
    path("players/<str:name>", login_required(views.player)),
    path("characters", login_required(CharacterListView.as_view())),
    path("character/add", login_required(views.addCharacter), name="newcharacter"),
    path("characters/edit/<int:id>", login_required(views.editCharacter), name="editcharacter"),
    path("loots", login_required(LootListView.as_view())),
    path("raids", login_required(RaidListView.as_view())),
    path("raid/add", login_required(views.addRaid), name="newraid"),
    path("raids/edit/<int:id>", login_required(views.editRaid), name="editraid"),
    path("epgp", login_required(EPGPLogEntryListView.as_view())),
    path("epgp/ranking", login_required(views.EPGPPlayerRanking), name="ranking"),
    path("epgp/giveraid", login_required(views.giveRaidEPGP), name="giveraid"),
    path("epgp/sessionloot", login_required(views.sessionLootEPGP), name="sessionloot"),
    path("epgp/sessionloot/<int:id>", login_required(views.sessionLootRaidEPGP), name="sessionlootraid"),
    path("epgp/decay", login_required(views.applyDecay), name="decay"),
    path("epgp/dock", login_required(views.applyDock), name="dock"),
    path("epgp/giveep", login_required(views.giveep), name="giveep"),
    path("epgp/standby", login_required(views.standby), name="standby"),
]
