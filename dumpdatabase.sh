 mysqldump epgp_test > "/home/github/dump_$(date '+%Y-%m-%d').sql"
 ls -tp /home/github/dump* | grep -v '/$' | tail -n +8 | xargs -I {} rm -- {}
