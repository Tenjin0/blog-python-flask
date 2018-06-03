
import sys
import time
from app import create_app, celery, socketio, db
from app.models import User, Post, Task

app = create_app()
app.app_context().push()


@celery.task(bind=True)
def longtime_add(self, x, y):
    print('long time task begins')
    time.sleep(3)
    self.update_state(state="PROGRESS", meta={'progress': 33})
    time.sleep(3)
    self.update_state(state="PROGRESS", meta={'progress': 66})
    time.sleep(3)
    print('long time task finished')
    return x + y


@celery.task(bind=True)
def export_posts_task(self, user_id, user_room):
    try:
        user = User.query.get(user_id)
        data = []
        i = 0
        total_posts = user.posts.count()
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({
                "body": post.body,
                "timestamp": post.timestamp.isoformat() + 'Z'
            })
            time.sleep(5)
            i += 1
            progress = 100 * i // total_posts
            self.update_state(state="PROGRESS", meta={'progress': progress})
            socketio.emit('task_update',
                          {'progress': progress, 'id': self.request.id},
                          room=user_room, namespace="/notifications")
            if progress >= 100:
                task = Task.query.get(self.request.id)
                if task is not None:
                    task.complete = True
                    db.session.commit()

        # send_email('[Microblog] Your blog posts',
        #            sender=app.config['ADMINS'][0], recipients=[user.email],
        #            text_body=render_template(
        #                'email/export_posts.txt', user=user),
        #            html_body=render_template(
        #                'email/export_posts.html', user=user),
        #            attachments=[('posts.json', 'application/json',
        #                          json.dumps({'posts': data}, indent=4))],
        #            sync=True)

    except Exception as e:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
