from django.urls import re_path, path
from django.contrib.auth.decorators import login_required

from . import views
from .views import *

ADMIN_VIEWS_PREFIX="administration/"

urlpatterns = [
    path("", views.index, name="home"),
    re_path(r'^.*\.html', views.pages, name='pages'),
    path("history", EPGPLogEntryListViewLight.as_view(), name="history"),
    path("progress", views.progress, name="progress"),
    path("ranking", views.EPGPPlayerRankingLight, name="rankingLight"),
    path("loots", LootListViewLight.as_view(), name="lootsLight"),
    path("rules", views.rules, name="rules"),
    path("player/<str:name>", views.player, name="player"),
    path("character/<str:name>", views.character, name="character"),
    path(ADMIN_VIEWS_PREFIX + "", views.indexAdmin, name="indexadmin"),
    path(ADMIN_VIEWS_PREFIX + "players", login_required(PlayerListView.as_view()), name="players"),
    path(ADMIN_VIEWS_PREFIX + "player/add", login_required(views.addPlayer), name="newplayer"),
    path(ADMIN_VIEWS_PREFIX + "player/disable/<str:name>", login_required(views.disablePlayer), name="disableplayer"),
    path(ADMIN_VIEWS_PREFIX + "characters", login_required(CharacterListView.as_view()), name="characters"),
    path(ADMIN_VIEWS_PREFIX + "character/add", login_required(views.addCharacter), name="newcharacter"),
    path(ADMIN_VIEWS_PREFIX + "characters/edit/<int:id>", login_required(views.editCharacter), name="editcharacter"),
    path(ADMIN_VIEWS_PREFIX + "loots", login_required(LootListView.as_view()), name="loots"),
    path(ADMIN_VIEWS_PREFIX + "raids", login_required(RaidListView.as_view()), name="raids"),
    path(ADMIN_VIEWS_PREFIX + "raid/add", login_required(views.addRaid), name="newraid"),
    path(ADMIN_VIEWS_PREFIX + "raids/edit/<int:id>", login_required(views.editRaid), name="editraid"),
    path(ADMIN_VIEWS_PREFIX + "epgp", login_required(EPGPLogEntryListView.as_view()), name="epgp"),
    path(ADMIN_VIEWS_PREFIX + "epgp/ranking", login_required(views.EPGPPlayerRanking), name="ranking"),
    path(ADMIN_VIEWS_PREFIX + "epgp/giveraid", login_required(views.giveRaidEPGP), name="giveraid"),
    path(ADMIN_VIEWS_PREFIX + "epgp/sessionloot", login_required(views.sessionLootEPGP), name="sessionloot"),
    path(ADMIN_VIEWS_PREFIX + "epgp/sessionloot/<int:id>", login_required(views.sessionLootRaidEPGP), name="sessionlootraid"),
    path(ADMIN_VIEWS_PREFIX + "epgp/decay", login_required(views.applyDecay), name="decay"),
    path(ADMIN_VIEWS_PREFIX + "epgp/dock", login_required(views.applyDock), name="dock"),
    path(ADMIN_VIEWS_PREFIX + "epgp/giveep", login_required(views.giveep), name="giveep"),
    path(ADMIN_VIEWS_PREFIX + "epgp/standby", login_required(views.standby), name="standby"),
    path(ADMIN_VIEWS_PREFIX + "epgp/reattribute/<int:id>", login_required(views.reattribute), name="reattribute"),
]
