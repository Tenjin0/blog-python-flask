from app import create_app, celery  # noqa: F401

app = create_app()
app.app_context().push()
