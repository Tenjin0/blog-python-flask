FROM python:latest

# RUN adduser -D myblog

WORKDIR /home/myblog

MAINTAINER Patrice PETIT <petitpatrice@gmail.com>
 
# Create the group and user to be used in this container
RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask

COPY . .
RUN pip install pipenv
# RUN pipenv install gunicorn
RUN pipenv install --system --deploy

ENV FLASK_APP blog.py

RUN chown -R flask:flaskgroup ./
RUN chmod +x boot.sh
USER flask
# ENTRYPOINT [ "source" "$(pipenv --venv)/bin/activate" ]
EXPOSE 5000
