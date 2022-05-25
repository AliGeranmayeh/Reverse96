#!/bin/sh
sleep 2
python manage.py makemigration;
python manage.py migrate;