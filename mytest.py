from datetime import datetime, timedelta

import unittest
from app import create_app, db
from app.models import User, Post
from config import Config
from  app.search import add_to_index, query_index, remove_from_index
current_app = create_app(Config)
current_app.app_context = current_app.app_context()
current_app.app_context.push()

posts = Post.query.all()
result = query_index(index='posts', query='post', page=1, per_page=4)
print(result)
