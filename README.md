# TriviaTrek

A flashcards website

# Setup

## Install dependencies

```sh
pip install .
```

## Run Redis

## Set up environment variables

Create a `.env` file in the root of the project with these contents

```env
SECRET_KEY=<secret key>
DJANGO_SETTINGS_MODULE='flashcards.settings_dev'
REDIS_URL='redis://redis:6379'
# See https://django-environ.readthedocs.io/en/latest/types.html#environ-env-db-url
DATABASE_URL="sqlite:////absolute/path/to/db/file.sqlite3"
```

## Run the server

```sh
python manage.py migrate
python manage.py runserver
```

## Run dramatiq

```sh
python manage.py rundramatiq
```

You should now be running a development server at `http://127.0.0.1:8000/`

> [!IMPORTANT]
> If after running `runserver` Django warns you about pending migrations, follow its instructions to fix it.

# Docker

Create a `.env` file in the root of the project with these contents

```env
SECRET_KEY=<secret key>
DJANGO_SETTINGS_MODULE='flashcards.settings_dev'
REDIS_URL='redis://redis:6379'
DB_DATABASE=<database>
DB_USER=<username>
DB_PASSWORD=<password>
# See https://django-environ.readthedocs.io/en/latest/types.html#environ-env-db-url
DATABASE_URL="mysql://<username>:<password>@db:3306/<database>"
```

Run Docker Compose

```sh
docker compose up
```

> [!IMPORTANT]
> You may want to clean up data during development for a variaty of reasons.
> For instance, some components may not like changes to environment variables.
> Changing the DB_PASSWORD in the environment might not change the password in the existing database, leading to authentication errors.
>
> You can erase all docker volumes associated with this project with `docker compose down -v`.
> **THIS WILL DESTROY ALL DATA**, so don't do it if you have anything important.