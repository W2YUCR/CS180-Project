# TriviaTrek

A flashcards website

# Setup

## Install dependencies

```sh
pip install .
```

## Run Redis

## Run the server

```sh
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
DJANGO_SETTINGS_MODULE='flashcards.settings_prod'
REDIS_URL='redis://redis:6379'
DB_DATABASE=<some database name>
DB_USER=<some username>
DB_PASSWORD=<some password>
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