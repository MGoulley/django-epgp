from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, FloatField, IntegerField
from django.db.models import F, Value
from django.db.models.functions import Round
from django.db.models.functions import Cast, Coalesce

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Joueur')
    discordTag = models.CharField(max_length=40, unique=True, verbose_name='Tag discord')
    isPU = models.BooleanField(default=False, verbose_name='Pick Up')
    isOfficier = models.BooleanField(default=False, verbose_name='Officier')
    isActive = models.BooleanField(default=True, verbose_name='Actif')

    objects = models.Manager()

    def __str__(self): 
         return self.name

class Character(models.Model):
    class CharacterRace(models.TextChoices):
        UNDEAD = "UNDEAD", _("Mort Vivant")
        TROLL = "TROLL", _("Troll")
        TAUREN = "TAUREN", _("Tauren")
        ORC = "ORC", _("Orc")
        GOBELIN = "GOBELIN", _("Gobelin")
        BLOODELF = "BLOODELF", _("Elf de Sang")

    class CharacterClass(models.TextChoices):
        DK = "DK", _("Chevalier de la mort")
        DRUID = "DRUID", _("Druide")
        HUNTER = "HUNTER", _("Chasseur")
        MAGE = "MAGE", _("Mage")
        PALADIN = "PALADIN", _("Paladin")
        PRIEST = "PRIEST", _("Pretre")
        ROGUE = "ROGUE", _("Voleur")
        SHAMAN = "SHAMAN", _("Chaman")
        WARLOCK = "WARLOCK", _("Demoniste")
        WARRIOR = "WARRIOR", _("Guerrier")

    class CharacterSpec(models.TextChoices):
        DPSCAC = "CAC", _("DPS Corps à Corps")
        DPSDIST = "DISTANT", _("DPS Distant")
        HEAL = "HEAL", _("Soigneur")
        TANK = "TANK", _("Tank")

    id = models.AutoField(primary_key=True)
    playerId = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="owner", verbose_name='Nom du Joueur')
    name = models.CharField(max_length=50, verbose_name='Nom du personnage')
    level = models.IntegerField(verbose_name='Niveau')
    ilvl = models.IntegerField(verbose_name="Niveau d'item")
    race = models.CharField(
        max_length=20,
        choices=CharacterRace,
        default=CharacterRace.ORC,
        verbose_name='Race',
    )
    classe = models.CharField(
        max_length=20,
        choices=CharacterClass,
        default=CharacterClass.MAGE,
        verbose_name='Classe',
    )
    specMain = models.CharField(
        max_length=20,
        choices=CharacterSpec,
        default=CharacterSpec.DPSDIST,
        verbose_name='Spécialisation principale',
    )
    specAlt = models.CharField(
        max_length=20,
        choices=CharacterSpec,
        default=CharacterSpec.DPSDIST,
        verbose_name='Spécialisation secondaire'
    )

    def __str__(self): 
         return self.name

class Loot(models.Model):
    inGameId = models.IntegerField(primary_key=True, verbose_name='ItemID')
    name = models.CharField(max_length=200, verbose_name='Nom')
    ilvl = models.IntegerField(verbose_name='Niveau item')
    gameSlot = models.IntegerField(verbose_name='Slot')

    @property
    def gpValue(self):
        variateur = 1.0
        match self.gameSlot:
            case 3 | 10 | 6 | 8 | 12 : 
                variateur = 0.7
            case 9 | 2 | 16 | 11 | 14 | 22 | 23 : 
                variateur = 0.5
            case 1 | 5 | 7 | 17 | 20 : 
                variateur = 1.0
            case 4 | 18 | 19 | 24 :
                variateur = 0.0
            case 13 | 15 | 21 | 25 | 26 | 28 :
                variateur = 0.4
            case 0 :
                variateur = 1.0
            case _  : 
                variateur = 1.0
        return int(round(variateur * self.ilvl, 0))
    
    @property
    def wowHeadUrl(self):
        baseUrl="https://www.wowhead.com/cata/fr/item="
        prefix = "<a href=\"" + baseUrl
        suffix = "\">WowHead</a>"
        return prefix + str(self.inGameId) + suffix
    
    @property
    def slot(self):
        slotName = ""
        match self.gameSlot:
            case 0 : 
                slotName = "Token/Monture"
            case 1 : 
                slotName = "Tête"
            case 2 : 
                slotName = "Cou"
            case 3 : 
                slotName = "Epaule"
            case 4 : 
                slotName = "Chemise"
            case 5 | 20 : 
                slotName = "Torse"
            case 6 : 
                slotName = "Ceinture"
            case 7 : 
                slotName = "Pantalon"
            case 8 : 
                slotName = "Pieds"
            case 9 : 
                slotName = "Brassards"
            case 10 : 
                slotName = "Mains"
            case 11 : 
                slotName = "Anneau"
            case 12 : 
                slotName = "Bijou"
            case 13 : 
                slotName = "Arme une main"
            case 14 : 
                slotName = "Bouclier"
            case 15 : 
                slotName = "Arc"
            case 16 : 
                slotName = "Cape"
            case 17 : 
                slotName = "Arme deux mains"
            case 18 : 
                slotName = "Sac"
            case 19 : 
                slotName = "Tabard"
            case 21 : 
                slotName = "Arme principale"
            case 22 | 23 : 
                slotName = "Off hand"
            case 24 : 
                slotName = "Munition"
            case 25 : 
                slotName = "Arme de Jet"
            case 26 : 
                slotName = "Distance"
            case 28 : 
                slotName = "Relique"
        return slotName

    def __str__(self): 
         return self.name + " (" + str(self.inGameId) + ")"

class Raid(models.Model):
    class RaidInstance(models.TextChoices):
        ICC = "ICC", _("Icecrown Citadel")
        BARADIN = "BARADIN", _("Baradin Hold")
        BASTION = "BASTION", _("Bastion of Twilight")
        THRONE = "THRONE", _("Throne of the Four Winds")
        BLACKWING = "BLACKWING", _("Blackwing Descent")
        FIRELAND = "FIRELAND", _("Firelands")
        DRAGON = "DRAGON", _("Dragon Soul")
        AUTRE = "AUTRE", _("Autre")

    id = models.AutoField(primary_key=True)
    played_at = models.DateField(verbose_name='Date', default=datetime.now)
    instance = models.CharField(
        max_length=20,
        choices=RaidInstance,
        default=RaidInstance.BARADIN,
        verbose_name='Instance',
    )
    participants = models.ManyToManyField(Character, verbose_name='Participants', related_name='participant')
    warcraftLogs = models.URLField(blank=True, null=True, max_length=200, verbose_name='URL Warcraft Logs')
    commentaire = models.CharField(blank=True, null=True, max_length=200, verbose_name='Commentaire')
    isClosed = models.BooleanField(default=False, verbose_name='Terminé')

    def __str__(self): 
         return self.instance + " " + str(self.played_at)

class EPGPLogEntryType(models.TextChoices):
        NEWPLAYER = "NEWPLAYER", _("Nouveau Joueur")
        DECAY = "DECAY", _("Decay")
        DOCKEP = "DOCKEP", _("Pénalité EP")
        DOCKGP = "DOCKGP", _("Pénalité GP")
        LOOT = "LOOT", _("Loot")
        PARTICIPATE = "PARTICIPATE", _("Participation")
        STANDBY = "STANDBY", _("Bench")
        OTHER = "OTHER", _("Autre")

class CustomEPGPLogEntryQuerySet(models.QuerySet):
    def getRankPerPlayerWithFilterActivePlayers(self):
        return self.filter(target_player__isActive=True).values("target_player__name").annotate(
                total_ep=Sum('ep_delta'), 
                total_gp=Sum('gp_delta')
            ).annotate(
                rank=Coalesce(Round(Cast(F('total_ep'), FloatField())/Cast(F('total_gp'), FloatField()), 3), Cast(F('total_ep'), FloatField()))
            ).order_by("-rank")
    
    def getRankPerPlayer(self):
        return self.values("target_player__name").annotate(
                total_ep=Sum('ep_delta'), 
                total_gp=Sum('gp_delta')
            ).annotate(
                rank=Coalesce(Round(Cast(F('total_ep'), FloatField())/Cast(F('total_gp'), FloatField()), 3), Cast(F('total_ep'), FloatField()))
            ).order_by("-rank")
    
    def getRankPerPlayerComplete(self):
        return self.values(name=F("target_player__name"), isPU=F("target_player__isPU")).annotate(
                total_ep=Sum('ep_delta'), 
                total_gp=Sum('gp_delta')
            ).annotate(
                rank=Coalesce(Round(Cast(F('total_ep'), FloatField())/Cast(F('total_gp'), FloatField()), 3), Cast(F('total_ep'), FloatField()))
            ).order_by("-rank")
    
    def getTotalEPPerPlayer(self, decay):
        return self.values("target_player").annotate(
                total_ep=Sum('ep_delta')
            ).annotate(
                decay=Cast((F("total_ep") * (Value(decay) / 100)), IntegerField())
            )

    def getRankPerCharacter(self):
        # TODO: Select EPGP par personnage
        return self.values("target_player__id").annotate(
                total_ep=Sum('ep_delta'), 
                total_gp=Sum('gp_delta')
            ).annotate(
                rank=Coalesce(Round(Cast(F('total_ep'), FloatField())/Cast(F('total_gp'), FloatField()), 3), Cast(F('total_ep'), FloatField()))
            ).order_by("-rank")

class EPGPLogEntry(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créée le')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modifié le')
    target_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_target_player', verbose_name='Joueur')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_user_id', verbose_name='Attributeur', default=1)
    type = models.CharField(
        max_length=20,
        choices=EPGPLogEntryType,
        default=EPGPLogEntryType.LOOT,
        verbose_name='Type',
    )
    raid = models.ForeignKey(Raid, on_delete=models.CASCADE, related_name='raid_raid', blank=True, null=True, verbose_name='Raid')
    reason = models.CharField(max_length=200, blank=True, null=True, verbose_name='Raison')
    loot_id = models.ForeignKey(Loot, on_delete=models.CASCADE, related_name="loot", blank=True, null=True)
    ep_delta = models.IntegerField(verbose_name='Modification en EP')
    gp_delta = models.IntegerField(verbose_name='Modification en GP')
    canceled = models.BooleanField(default=False, verbose_name='Validité')
    canceled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_canceled_by', blank=True, null=True, verbose_name='Annulé par')

    objects = CustomEPGPLogEntryQuerySet.as_manager()

    def __str__(self): 
         return str(self.user_id) + " accorde " + str(self.ep_delta) + " EP et " +  str(self.gp_delta) + " GP à " + str(self.target_player) + " " + str(self.loot_id)



