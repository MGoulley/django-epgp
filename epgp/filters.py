from django_filters import FilterSet
from .models import *

class LootFilter(FilterSet):
    class Meta:
        model = Loot
        fields = {"name": ["contains"], "inGameId": ["exact"]}
