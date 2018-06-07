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
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    }
)

components = {
  "securitySchemes": {
    "bearerAuth": {
      "type": "http",
      "scheme": "bearer",
      "bearerFormat": "JWT"
    } 
  }
}

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
    components=components
)

app = create_app()
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
cli.register(app)

from app.api.users import get_user
from app.api.schemas import UserApiSchema, LinkSchema
spec.definition('Links', schema=LinkSchema)
spec.definition('User', schema=UserApiSchema)

with app.test_request_context():
    spec.add_path(view=get_user)

# We're good to: go! Save this to a file for now.
with open('app/static/swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f, indent=4)


@app.shell_context_processor
def make_shell_context():
    print('make_shell_context')
    Post.search("post", 1, 3)
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            "Notification": Notification, 'Task': Task}


if __name__ == "__main__":
    socketio.run(debug=True)
