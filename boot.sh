#!/bin/sh
source $(pipenv --venv)/bin/activate
flask db upgrade
# flask translate compile
flask run
# exec gunicorn -b :5000 --access-logfile - --error-logfile - myblog:app