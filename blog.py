from app import db, cli, create_app
from app.models import User, Post, Message, Notification, Task


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    print('make_shell_context')
    Post.search("post", 1, 3)
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            "Notification": Notification, 'Task': Task}


if __name__ == "__main__":
    app.socketio.run(debug=True)
