#!/bin/bash
set -x

echo "Copie dans systemd"
cp /opt/lbdb/django/lbdb-django.service /etc/systemd/system/
systemctl --user enable lbdb-django.service
