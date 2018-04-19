#!/usr/bin/env bash

# run migrations
echo "Running migrations..."
python manage.py showmigrations
python manage.py migrate
python manage.py showmigrations

# load default data
echo "Creating default user..."
python manage.py createdefaultsuperuser

echo "Creating default sms alert configurations..."
python manage.py createsmsalert

echo "Load development data from fixtures..."
python manage.py loaddata localisation_data.json
python manage.py loaddata development_fixture.json
