from app import db, cli, create_app
from app.models import User, Post


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    print('make_shell_context')
    Post.search("post", 1, 3)
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == "__main__":
    app.run(debug=True)
