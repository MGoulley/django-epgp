import django_tables2 as tables
from .models import *

class PlayerTable(tables.Table):
    class Meta:
        model = Player
        fields = ("name", "discordTag")
        #fields = ("name", "discordTag", "owner__name")

class CharacterTable(tables.Table):
    class Meta:
        model = Character
        fields = ("name", "level", "ilvl", "race", "classe", "specMain", "specAlt", "playerId__name")

class LootTable(tables.Table):
    gpValue = tables.Column("Valeur en GP", accessor=tables.A('gpValue'), orderable=True)
    wowHeadUrl = tables.TemplateColumn(verbose_name="Lien WowHead", template_code='<a href="https://www.wowhead.com/cata/item={{record.inGameId}}">WowHead</a>')
    slot = tables.Column("Slot", accessor=tables.A('slot'), orderable=True)
    class Meta:
        model = Loot
        fields = ("name", "ilvl", "slot", "gpValue", "wowHeadUrl")
        order_by = '-ilvl'

class EPGPLogEntryTable(tables.Table):
    wowHeadUrl = tables.TemplateColumn(verbose_name="Lien WowHead", template_code='<a href="https://www.wowhead.com/cata/item={{record.loot_id.inGameId}}">WowHead</a>')
    class Meta:
        model = EPGPLogEntry
        fields = ("id", "updated_at", "created_at", "target_player_id", "type", "reason", "wowHeadUrl", "ep_delta", "gp_delta", "source_player_id", "canceled", "canceled_by")
        order_by = '-updated_at'

class RaidTable(tables.Table):
    class Meta:
        model = Raid
        fields = ("played_at", "instance", "participants", "commentaire")
        order_by = '-played_at'
