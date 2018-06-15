#!/bin/sh
source $(pipenv --venv)/bin/activate
flask db upgrade
flask translate compile
flask run --host=0.0.0.0
# exec gunicorn -b :5000 --access-logfile - --error-logfile - myblog:app
