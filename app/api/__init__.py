from flask import Blueprint, render_template
# from flask_restful import Api
# from app.api.helloworld import HelloWorld  # noqa: F401

bp = Blueprint('api', __name__)

from app.api import users, errors, tokens  # noqa: F401


@bp.route('/', methods=['GET'])
def api_swagger():
    return render_template("swagger.html")
# api = Api(bp, prefix="/api")
# api.add_resource(HelloWorld, "/helloworld")
