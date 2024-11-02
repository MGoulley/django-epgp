from django_filters import FilterSet
from .models import *
from django.db.models import F, Value

class CharacterFilterIsActive(FilterSet):
    class Meta:
        model = Character
        fields = {"playerId__isActive": ["exact"]}

class LootFilter(FilterSet):
    class Meta:
        model = Loot
        fields = {"name": ["contains"], "inGameId": ["exact"]}

class EPGPFilter(FilterSet):
    class Meta:
        model = EPGPLogEntry
        fields = {"target_player": ["exact"], "raid": ["exact"], "target_player__isActive": ["exact"]}

