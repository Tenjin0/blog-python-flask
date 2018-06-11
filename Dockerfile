FROM python:3.6-alpine

RUN adduser -D myblog

WORKDIR /home/myblog

COPY app app
COPY migrations migrations
COPY Pipfile Pipfile.lock blog.py config.py celery_worker.py boot.sh ./
RUN pip install pipenv
# RUN pipenv install gunicorn
RUN pipenv install --system


ENV FLASK_APP microblog.py
ENV FLASK_ENV development

RUN chown -R myblog:myblog ./
RUN chmod +x boot.sh

USER myblog

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]
