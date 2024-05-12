from django_filters import FilterSet
from .models import *

class LootFilter(FilterSet):
    class Meta:
        model = Loot
        fields = {"name": ["exact", "contains"], "inGameId": ["exact"]}
