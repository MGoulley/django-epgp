# TODO
PROD READY : https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


TODO List:
- Faire une page joueur : EP GP avec son évolution, liste de ses personnages
- Faire une page de personnage : Affichage du personnage, 

# Roadmap
!epgp.decay - Performs EPGP decay on all players.
!epgp.dock <ep:int> <reason:string> <...character:string> - Removes EP for poor performance.
!epgp.dockgp <gp:int> <reason:string> <...character:string> - Awards GP for poor performance.
!epgp.award.incentive <ep:int> <reason:string> <...character:string> - Awards EP for non-raid reasons.
!epgp.award.standby <ep:int> <raid:string> <...character:string> [--note <:string>] [--skip <...character:string>] - Awards EP for standing by for a raid.
!item.distribution <item:string> <raid:string> [<...character:string>] [--min-clears <n:int>] [--raid-size <n:int>] - Tool to help distribute a piece of loot evenly amongst players.
!character.update <character:string> [--level <:int> --race <:string> --class <:string> --guild <:string> --spec1 <:string> --spec2 <:string>] - Updates character information manually.
!epgp.loot.backfill Un Joueur donne un item à un autre joueur
!epgp.totals [--sort <'EP'|'GP'|'ITEMS'|'PRIORITY'(default)>] - Display EPGP standings with total EPGP earned.
!epgp [<character:string>] - Displays EPGP for a character.
!epgp.compare <...character:string> [--details] - Compares EPGP across multiple characters.
!player.character.list <player:string> - Lists a player's characters.
!character.whocanplay [--class <...:string>] [--spec <...:string>] [--role <'healer'|'tank'|'dps'>] [--alts-of <...character:string>] - Displays who is able to play a particular class, spec, or role.
!equip <character:string> <...item:string> - Equips item(s) to a character in the UI.
