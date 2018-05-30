from app import celery, create_app


app = create_app()
app.app_context().push()
print(app.config["CELERY_BROKER_URL"])
