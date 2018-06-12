import json
from app import db, cli, create_app, socketio
from app.models import User, Post, Message, Notification, Task
from apispec import APISpec
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api'
API_URL = 'http://localhost:5000/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Test application"
    }
)

spec = APISpec(
    title='My Awesome API',
    version='1.0.42',
    info=dict(
        description='You know, for devs'
    ),
    plugins=[
        'apispec.ext.flask',
        'apispec.ext.marshmallow'
    ],
    openapi_version="3.0",
    securityDefinitions={
        "bearerAuth": {
            "description": "",
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
)

app = create_app()
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
cli.register(app)

from app.api.users import get_user, get_users   # noqa: F401
from app.api.users import create_user, update_user   # noqa: F401
from app.api.users import get_followers, get_followed  # noqa: F401
from app.api.tokens import get_token  # noqa: F401
from app.api.schemas.users import LinkSchema, UserListApiSchema  # noqa: F401
from app.api.schemas.users import UserApiSchema, MetaSchema  # noqa: F401
from app.api.schemas.users import UserPostApiSchema  # noqa: F401
from app.api.schemas.users import UserPutApiSchema  # noqa: F401
from app.api.schemas.users import TokenApiSchema  # noqa: F401
spec.definition('User', schema=UserApiSchema)
spec.definition('Users', schema=UserListApiSchema)
spec.definition('Links', schema=LinkSchema)
spec.definition('Meta', schema=MetaSchema)
spec.definition('CreateUser', schema=UserPostApiSchema)
spec.definition('UpdateUser', schema=UserPutApiSchema)
spec.definition('Token', schema=TokenApiSchema)

with app.test_request_context():
    spec.add_path(view=get_user)
    spec.add_path(view=get_users)
    spec.add_path(view=get_followers)
    spec.add_path(view=get_followed)
    spec.add_path(view=create_user)
    spec.add_path(view=update_user)
    spec.add_path(view=get_token)

# We're good to: go! Save this to a file for now.
with open('app/static/swagger.json', 'w') as f:
    spec_gen = spec.to_dict()
    spec_gen['components']['securitySchemes'] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        },
        "basicAuth": {
            "type": "http",
            "scheme": "basic"
        }
    }
    json.dump(spec_gen, f, indent=4)


@app.shell_context_processor
def make_shell_context():
    print('make_shell_context')
    Post.search("post", 1, 3)
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            "Notification": Notification, 'Task': Task}


if __name__ == "__main__":
    socketio.run(host='0.0.0.0')
