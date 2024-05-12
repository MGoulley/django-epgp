from django.urls import re_path, path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("players", PlayerListView.as_view()),
    path("players/<str:name>", views.player),
    path("characters", CharacterListView.as_view()),
    path("loots", LootListView.as_view()),
    path("raids", RaidListView.as_view()),
    path("epgp", EPGPLogEntryListView.as_view()),
    path("epgp/giveraid", views.giveRaidEPGP, name="giveraid"),
    path("epgp/giveloot", views.giveLootEPGP, name="giveloot"),
    re_path(r'^loot-autocomplete/$', LootAutocomplete.as_view(), name='loot-autocomplete',),
    re_path(r'^loot-autocomplete/<str:q>$', LootAutocomplete.as_view(model=Loot), name='loot-autocomplete',),
]
