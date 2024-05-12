from django.urls import include, path

from . import views
from .views import *
from crudbuilder import urls

urlpatterns = [
    path("", views.index, name="index"),
    path("players", PlayerListView.as_view()),
    path("players/<str:name>", views.player, name="player"),
    path("characters", CharacterListView.as_view()),
    path("loots", views.lootListView(None)),
    path("raids", RaidListView.as_view()),
    path("epgp", EPGPLogEntryListView.as_view()),
    path("epgp/give", views.giveEPGP, name="giveEPGP"),
]
