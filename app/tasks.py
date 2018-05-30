
import json
import sys
import time
from flask import render_template
from app import create_app, db, celery
from app.celery import current_task
from app.models import User, Post, Task
from app.email import send_email

app = create_app()
app.app_context().push()


@celery.task
def longtime_add(x, y):
    print('long time task begins')
    # sleep 10 seconds
    time.sleep(10)
    print('long time task finished')
    return x + y


@celery.task
def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        data = []
        i = 0
        # total_posts = user.posts.count()
        for post in user.posts.orderby(Post.timestamp.asc()):
            data.append({
                "body": post.body,
                "timestamp": post.timestamp.isoformat() + 'Z'
            })
            time.sleep(5)
            i += 1
        send_email('[Microblog] Your blog posts',
                   sender=app.config['ADMINS'][0], recipients=[user.email],
                   text_body=render_template(
                       'email/export_posts.txt', user=user),
                   html_body=render_template(
                       'email/export_posts.html', user=user),
                   attachments=[('posts.json', 'application/json',
                                 json.dumps({'posts': data}, indent=4))],
                   sync=True)

    except Exception as e:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
