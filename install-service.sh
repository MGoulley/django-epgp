#!/bin/bash
set -x

echo "Copie dans systemd"
cp /opt/lbdb/django/lbdb-django.service ~/.config/systemd/user/
systemctl --user enable lbdb-django.service
systemctl --user daemon-reload
