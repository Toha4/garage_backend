#!/bin/bash

source /home/www/.virtualenvs/garage/bin/activate
cd /home/www/garage_backend/src
python manage.py sync_cars --no_log_cmd
python manage.py sync_employees --no_log_cmd
deactivate