#!/bin/bash
set -x

cat nginx.conf > /etc/nginx/sites-available/lbdb_nginx.conf
sudo ln -s /etc/nginx/sites-available/lbdb_nginx.conf /etc/nginx/sites-enabled/
