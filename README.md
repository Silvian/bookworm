# Bookworm

[![Build Status](https://travis-ci.org/Silvian/bookworm.svg?branch=master)](https://travis-ci.org/Silvian/bookworm) ![AUR](https://img.shields.io/aur/license/yaourt.svg) ![PyPI - Django Version](https://img.shields.io/pypi/djversions/djangorestframework.svg)

A simple books archiving application with reading list and notifications feature.
Includes book reading progress tracking, multi user support and SMS Alerts notifications reminding you to pick up where you've left off.

#### Contributors: Silvian Dragan and Laurence Green
##### Published under GNU General Public Licence v3 - please read the LICENSE included.



# Installation Guide:

This project is dockerized so the following guide will highlight the requirements and steps needed to run in a docker environment.

Install docker and docker-compose specific to your operating system. See https://www.docker.com for more details.

git clone the project and in the project base directory create a .env file with the following inside:

`DATABASE_HOST=postgres`

`DATABASE_NAME=postgres`

`DATABASE_USER=postgres`

`DATABASE_PASSWORD=postgres`

Inside the project base directory where docker-compose.yml file can be found, run the following commands:
*docker-compose up --build*

Once the process has finished and the postgres sql database and application are running, run the migrations and load data command inside docker as following:
*docker-compose run --rm web scripts/migrate_loaddata.sh*

This also creates a default user: *root* with password: *root*

Login to the django administration page at: http://localhost:8000/admin/ with the credentials above to verify this.

Note: you can login with the default user created here at http://localhost:8000/ or create other users via django admin panel.


# Tests:

To run the test pack simply run:
*./scripts/test.sh*


# Search:

Applied to books
*http://localhost:8000/books/book/?search=pride*
