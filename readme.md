# TODO
PROD READY : https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Roadmap

Ajouter liste des raids avec les boss

Changer la valeur des tokens
Fix le +2 à 10% du prix normal
Ajout Pick Up oui/non
!item.distribution <item:string> <raid:string> [<...character:string>] [--min-clears <n:int>] [--raid-size <n:int>] - Tool to help distribute a piece of loot evenly amongst players.
!epgp.totals [--sort <'EP'|'GP'|'ITEMS'|'PRIORITY'(default)>] - Display EPGP standings with total EPGP earned.
!epgp [<character:string>] - Displays EPGP for a character.
!epgp.compare <...character:string> [--details] - Compares EPGP across multiple characters.
!Decay en GP
!character.whocanplay [--class <...:string>] [--spec <...:string>] [--role <'healer'|'tank'|'dps'>] [--alts-of <...character:string>] - Displays who is able to play a particular class, spec, or role.
Faire une page joueur : EP GP avec son évolution, liste de ses personnages
Faire une page de personnage : Affichage du personnage,
!equip <character:string> <...item:string> - Equips item(s) to a character in the UI.
Pouvoir lier LogEPGP avec un raid


# Démarrer éteindre le service

systemctl --user status lbdb-django
systemctl --user start lbdb-django
systemctl --user stop lbdb-django

# Mettre en place le dump mysql
crontab -e
0 1 * * * /opt/lbdb/django/dumpdatabase.sh
