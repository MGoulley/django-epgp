#!/bin/bash
set -x

source .venv/bin/activate

python3.11 manage.py check --deploy
#python3.11 manage.py runserver 0.0.0.0:80
uwsgi --ini lbdb_uwsgi.ini
