from django.urls import re_path, path
from django.contrib.auth.decorators import login_required

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("players", PlayerListView.as_view()),
    path("player/add", login_required(views.addPlayer), name="newplayer"),
    path("players/<str:name>", views.player),
    path("characters", CharacterListView.as_view()),
    path("character/add", login_required(views.addCharacter), name="newcharacter"),
    path("loots", LootListView.as_view()),
    path("raids", login_required(RaidListView.as_view())),
    path("raid/add", login_required(views.addRaid), name="newraid"),
    path("epgp", EPGPLogEntryListView.as_view()),
    path("epgp/ranking", views.EPGPPlayerRanking, name="ranking"),
    path("epgp/giveraid", login_required(views.giveRaidEPGP), name="giveraid"),
    path("epgp/giveloot", login_required(views.giveLootEPGP), name="giveloot"),
    path('loot-autocomplete/', LootAutocomplete.as_view(model=Loot), name='loot-autocomplete',),
    path('loot-autocomplete/<str:q>', LootAutocomplete.as_view(model=Loot), name='loot-autocomplete',),
]
