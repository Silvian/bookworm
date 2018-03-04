#!/usr/bin/env bash

sleep 2
dockerize -wait tcp://postgres:5432 -timeout 60s python manage.py runserver 0.0.0.0:8000
