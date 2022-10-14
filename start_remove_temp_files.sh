#!/bin/bash
source /home/www/.virtualenvs/garage/bin/activate
cd /home/www/garage_backend/src
python manage.py remove_temp_files
deactivate