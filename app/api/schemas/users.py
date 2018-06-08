
from marshmallow import Schema, fields


class LinkSchema(Schema):
    self = fields.Url()
    followers = fields.Url()
    followed = fields.Url()
    avatar = fields.Url()


class MetaSchema(Schema):
    page = fields.Int()
    per_page = fields.Int()
    total_items = fields.Int()
    total_pages = fields.Int()


class UserApiSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True)
    last_seen = fields.Date()
    about_me = fields.Str(required=True)
    post_count = fields.Int()
    follower_count = fields.Int()
    followed_count = fields.Int()
    _links = fields.Nested(LinkSchema)


class UserListApiSchema(Schema):
    items = fields.Nested(UserApiSchema, many=True)
    _meta = fields.Nested(MetaSchema)
    _links = fields.Nested(LinkSchema)

# 'id': self.id,
# 'username': self.username,
# 'last_seen': self.last_me.isoformat() + 'Z'
# if self.last_me is not None else None,
# 'about_me': self.about_me,
# 'post_count': self.posts.count(),
# 'follower_count': self.followers.count(),
# 'followed_count': self.followed.count(),
# '_links': {
#     'self': url_for('api.get_user', id=self.id),
#     'followers': url_for('api.get_followers', id=self.id),
#     'followed': url_for('api.get_followed', id=self.id),
#     'avatar': self.avatar(128)