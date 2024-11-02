import django_tables2 as tables
from .models import *

class PlayerTable(tables.Table):
    name = tables.TemplateColumn(verbose_name="Joueur", template_code='<a href="/player/{{record.name}}">{{record.name}}</a>', orderable=True)
    disable = tables.TemplateColumn(verbose_name="Est Inactif", template_code='<a href="/administration/player/disable/{{record.name}}">Tagger comme inactif</a>', orderable=False)
    class Meta:
        model = Player
        fields = ("name", "discordTag", "isOfficier", "isPU", "isActive", "disable")
    
    def before_render(self, request):
        if not request.user.is_authenticated:
            self.columns.hide('discordTag')

class CharacterTable(tables.Table):
    name = tables.TemplateColumn(verbose_name="Joueur", template_code='<a href="/character/{{record.name}}">{{record.name}}</a>', orderable=True)
    edit = tables.TemplateColumn(verbose_name="Edit", template_code='<a href="{{ request.path }}/edit/{{record.id}}">Edit</a>', orderable=False)
    class Meta:
        model = Character
        fields = ("name", "level", "ilvl", "race", "classe", "specMain", "specAlt", "playerId__name", "edit")

    def before_render(self, request):
        if not request.user.is_authenticated:
            self.columns.hide('edit')

class CharacterTableLight(tables.Table):
    name = tables.TemplateColumn(verbose_name="Joueur", template_code='<a href="/character/{{record.name}}">{{record.name}}</a>', orderable=True)
    class Meta:
        model = Character
        fields = ("name", "level", "race", "classe", "specMain", "specAlt")
        row_attrs = {
            "class": lambda record: "table-" + record.classe.lower()
        }

class EPGPRankTable(tables.Table):
    joueur = tables.TemplateColumn(verbose_name="Joueur", template_code='<a href="/player/{{record.target_player__name}}">{{record.target_player__name}}</a>', orderable=True)
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
    reattribute = tables.TemplateColumn(verbose_name="Réattribuer", template_code='<a href="{{ request.path }}/reattribute/{{record.id}}">Réattribuer</a>', orderable=False)
    class Meta:
        model = EPGPLogEntry
        fields = ("id", "updated_at", "created_at", "target_player", "raid", "type", "reason", "wowHeadUrl", "ep_delta", "gp_delta", "user_id", "canceled", "canceled_by", "reattribute")
        order_by = '-updated_at'

    def before_render(self, request):
        if not request.user.is_authenticated:
            self.columns.hide('reattribute')

class EPGPLogEntryTableLight(tables.Table):
    target_player = tables.TemplateColumn(verbose_name="Joueur", template_code='<a href="/player/{{record.target_player.name}}">{{record.target_player.name}}</a>', orderable=True)
    wowHeadUrl = tables.TemplateColumn(verbose_name="Lien WowHead", template_code='{% if record.loot_id.inGameId %} <a href="https://www.wowhead.com/cata/fr/item={{record.loot_id.inGameId}}">WowHead</a>{% endif%}', orderable=False)
    class Meta:
        model = EPGPLogEntry
        fields = ("created_at", "target_player", "raid", "type", "reason", "wowHeadUrl", "ep_delta", "gp_delta")
        order_by = '-created_at'

class EPGPLogEntryRaidTable(tables.Table):
    created_at = tables.columns.TemplateColumn(template_code=u"""{{ record.created_at }}""", orderable=True, verbose_name='Date')
    target_player__name = tables.columns.TemplateColumn(template_code=u"""{{ record.target_player__name }}""", orderable=True, verbose_name='Joueur')
    reason = tables.columns.TemplateColumn(template_code=u"""{{ record.reason }}""", orderable=True, verbose_name='Attribution')
    wowHeadUrl = tables.TemplateColumn(verbose_name="Lien WowHead", template_code='{% if record.loot_id %} <a href="https://www.wowhead.com/cata/fr/item={{record.loot_id}}">WowHead</a>{% endif%}', orderable=False)
    
    def get_caption_display(self):
        return False

    class Meta:
        fields = ('created_at', 'target_player__name', 'reason', 'wowHeadUrl')
        sequence = fields
        order_by = 'target_player__name'

class RaidTable(tables.Table):
    edit = tables.TemplateColumn(verbose_name="Edit", template_code='<a href="{{ request.path }}/edit/{{record.id}}">Edit</a>', orderable=False)
    class Meta:
        model = Raid
        fields = ("played_at", "instance", "participants", "warcraftLogs", "commentaire", "isClosed", "edit")
        order_by = '-played_at'
    
    def before_render(self, request):
        if not request.user.is_authenticated:
            self.columns.hide('edit')
