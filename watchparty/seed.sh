#!/bin/bash
rm -rf watchpartyapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations watchpartyapi
python3 manage.py migrate watchpartyapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata fans
python3 manage.py loaddata sporttypes
python3 manage.py loaddata games
python3 manage.py loaddata watchparties