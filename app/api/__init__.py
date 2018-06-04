from flask import Blueprint
from flask_restful import Api
from app.api.helloworld import HelloWorld  # noqa: F401

bp = Blueprint('api', __name__)
api = Api(bp, prefix="/api")
api.add_resource(HelloWorld, "/helloworld")