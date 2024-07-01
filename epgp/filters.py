from django_filters import FilterSet
from .models import *

class LootFilter(FilterSet):
    class Meta:
        model = Loot
        fields = {"name": ["contains"], "inGameId": ["exact"]}

class EPGPFilter(FilterSet):
    class Meta:
        model = EPGPLogEntry
        fields = {"target_player": ["exact"], "raid": ["exact"]}

class EPGPRankFilter(FilterSet):
    class Meta:
        model = Player
        fields = {"name": ["exact"], "isPU": ["exact"]}
