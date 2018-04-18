#!/usr/bin/env bash

export DJANGO_SETTINGS_MODULE=bookworm.settings

dockerize -wait tcp://postgres:5432 -timeout 60s gunicorn bookworm.wsgi:application \
    --name bookworm \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=debug \
"$@"
