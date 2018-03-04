#!/usr/bin/env bash

# run migrations
echo "Running migrations..."
python manage.py showmigrations
python manage.py migrate
python manage.py showmigrations

# load default data
echo "Creating default user..."
python manage.py createdefaultsuperuser
