# Bookworm
Books reading list and reviews application


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
*docker-compose run --rm web python manage.py test*