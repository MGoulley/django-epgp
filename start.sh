#!/bin/bash
set -x

source /opt/lbdb/django/venv/bin/activate
/opt/lbdb/django/venv/bin/python3.11 /opt/lbdb/django/manage.py runserver 0.0.0.0:8000
