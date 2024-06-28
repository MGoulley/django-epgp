# TODO
PROD READY : https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Roadmap

!epgp.totals [--sort <'EP'|'GP'|'ITEMS'|'PRIORITY'(default)>] - Display EPGP standings with total EPGP earned.
!epgp [<character:string>] - Displays EPGP for a character.
!epgp.compare <...character:string> [--details] - Compares EPGP across multiple characters.
!Decay en GP
!character.whocanplay [--class <...:string>] [--spec <...:string>] [--role <'healer'|'tank'|'dps'>] [--alts-of <...character:string>] - Displays who is able to play a particular class, spec, or role.
Faire une page joueur : EP GP avec son évolution, liste de ses personnages
Faire une page de personnage : Affichage du personnage,
!equip <character:string> <...item:string> - Equips item(s) to a character in the UI.
Ajouter liste des raids avec les boss


# superlien
Pour générer du css custom color: https://lingtalfi.com/bootstrap4-color-generator

# couleurs classe
.dk input:checked + span{background-color: #C41E3A;}
.druid input:checked + span{background-color: #FF7C0A;}
.hunter input:checked + span{background-color: #AAD372;}
.mage input:checked + span{background-color: 	#3FC7EB;}
.paladin input:checked + span{background-color: #F48CBA;}
.priest input:checked + span{background-color: #FFFFFF;}
.rogue input:checked + span{background-color: #FFF468;}
.shaman input:checked + span{background-color: #0070DD;}
.warlock input:checked + span{background-color:	#8788EE;}
.warrior input:checked + span{background-color:	#C69B6D;}

# Démarrer éteindre le service

systemctl --user status lbdb-django
systemctl --user start lbdb-django
systemctl --user stop lbdb-django

# Mettre en place le dump mysql
crontab -e
0 1 * * * /opt/lbdb/django/dumpdatabase.sh
