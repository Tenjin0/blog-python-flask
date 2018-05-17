from app import app, db
from app.models import User, Post
from app import cli # noqa: E261, F401


@app.shell_context_processor
def make_shell_context():
    print('make_shell_context')
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == "__main__":
    app.run(debug=True)
