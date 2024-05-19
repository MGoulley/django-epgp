from django.urls import re_path, path
from django.contrib.auth.decorators import login_required

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.index, name="home"),
    re_path(r'^.*\.html', views.pages, name='pages'),
    path("players", PlayerListView.as_view()),
    path("player/add", login_required(views.addPlayer), name="newplayer"),
    path("players/<str:name>", views.player),
    path("characters", CharacterListView.as_view()),
    path("character/add", login_required(views.addCharacter), name="newcharacter"),
    path("characters/edit/<int:id>", login_required(views.editCharacter), name="editcharacter"),
    path("loots", LootListView.as_view()),
    path("raids", login_required(RaidListView.as_view())),
    path("raid/add", login_required(views.addRaid), name="newraid"),
    path("epgp", EPGPLogEntryListView.as_view()),
    path("epgp/ranking", views.EPGPPlayerRanking, name="ranking"),
    path("epgp/giveraid", login_required(views.giveRaidEPGP), name="giveraid"),
    path("epgp/giveloot", login_required(views.giveLootEPGP), name="giveloot"),
    path("epgp/decay", login_required(views.applyDecay), name="decay"),
    path("epgp/dock", login_required(views.applyDock), name="dock"),
    path("epgp/giveep", login_required(views.giveep), name="giveep"),
    path("epgp/standby", login_required(views.standby), name="standby"),
]
