import django_tables2 as tables
from .models import *

class PlayerTable(tables.Table):
    class Meta:
        model = Player
        fields = ("name", "discordTag", "isOfficier")
    
    def before_render(self, request):
        if not request.user.is_authenticated:
            self.columns.hide('discordTag')

class CharacterTable(tables.Table):
    edit = tables.TemplateColumn(verbose_name="Edit", template_code='<a href="{{ request.path }}/edit/{{record.id}}">Edit</a>', orderable=False)
    class Meta:
        model = Character
        fields = ("name", "level", "ilvl", "race", "classe", "specMain", "specAlt", "playerId__name", "edit")

    def before_render(self, request):
        if not request.user.is_authenticated:
            self.columns.hide('edit')

class EPGPRankTable(tables.Table):
    joueur = tables.columns.TemplateColumn(template_code=u"""{{ record.target_player__name }}""", orderable=True, verbose_name='Joueur')
    total_ep = tables.columns.TemplateColumn(template_code=u"""{{ record.total_ep }}""", orderable=True, verbose_name='Total EP')
    gp = tables.columns.TemplateColumn(template_code=u"""{{ record.total_gp }}""", orderable=True, verbose_name='Total GP')
    ranking = tables.columns.TemplateColumn(template_code=u"""{{ record.rank }}""", orderable=True, verbose_name='Ratio EP/GP')
    
    def get_caption_display(self):
        return False

    class Meta:
        fields = ('joueur', 'total_ep', 'gp', 'ranking')
        sequence = fields
        order_by = '-ranking'

class LootTable(tables.Table):
    gpValue = tables.Column("Valeur en GP", accessor=tables.A('gpValue'), orderable=False)
    wowHeadUrl = tables.TemplateColumn(verbose_name="Lien WowHead", template_code='<a href="https://www.wowhead.com/cata/fr/item={{record.inGameId}}">WowHead</a>', orderable=False)
    slot = tables.Column("Slot", accessor=tables.A('slot'), orderable=False)
    class Meta:
        model = Loot
        fields = ("name", "ilvl", "slot", "gpValue", "wowHeadUrl")
        order_by = '-ilvl'

class EPGPLogEntryTable(tables.Table):
    wowHeadUrl = tables.TemplateColumn(verbose_name="Lien WowHead", template_code='{% if record.loot_id.inGameId %} <a href="https://www.wowhead.com/cata/fr/item={{record.loot_id.inGameId}}">WowHead</a>{% endif%}', orderable=False)
    class Meta:
        model = EPGPLogEntry
        fields = ("id", "updated_at", "created_at", "target_player", "raid", "type", "reason", "wowHeadUrl", "ep_delta", "gp_delta", "user_id", "canceled", "canceled_by")
        order_by = '-updated_at'

class EPGPLogEntryTableLight(tables.Table):
    wowHeadUrl = tables.TemplateColumn(verbose_name="Lien WowHead", template_code='{% if record.loot_id.inGameId %} <a href="https://www.wowhead.com/cata/fr/item={{record.loot_id.inGameId}}">WowHead</a>{% endif%}', orderable=False)
    class Meta:
        model = EPGPLogEntry
        fields = ("created_at", "target_player", "raid", "type", "reason", "wowHeadUrl", "ep_delta", "gp_delta")
        order_by = '-created_at'

class RaidTable(tables.Table):
    edit = tables.TemplateColumn(verbose_name="Edit", template_code='<a href="{{ request.path }}/edit/{{record.id}}">Edit</a>', orderable=False)
    class Meta:
        model = Raid
        fields = ("played_at", "instance", "participants", "warcraftLogs", "commentaire", "isClosed", "edit")
        order_by = '-played_at'
    
    def before_render(self, request):
        if not request.user.is_authenticated:
            self.columns.hide('edit')
