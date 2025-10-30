# Institutional Database

This is a small demonstration of how institutional knowledge may be stored in a database.
Django provides a convenient admin interface to edit data.

## Getting Started

* Clone the repo

Install dependencies, the most simple way is with `uv`:

    uv sync

Then activate the virtual environment created by sync

    source .venv/bin/activate

Apply all migrations. This will create a `db.sqlite3` which acts as local database

    python manage.py migrate

With a database, create the admin account, answering the questions posed by:

    python manage.py createsuperuser

Finally run the project with

    python manage.py runserver

Access it at http://127.0.0.1:8000/admin/ and log in with the credentials created above.
