FROM python:latest

RUN adduser myblog

WORKDIR /home/myblog

COPY app app
COPY migrations migrations
COPY Pipfile Pipfile.lock blog.py config.py celery_worker.py boot.sh .env ./
RUN pip install pipenv
# RUN pipenv install gunicorn
RUN pipenv install


ENV FLASK_APP blog.py
ENV FLASK_ENV development

RUN chown -R myblog:myblog ./
RUN chmod +x boot.sh

USER myblog

EXPOSE 5000
