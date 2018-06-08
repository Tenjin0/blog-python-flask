
from app.api import bp
from flask import jsonify
from app.models import User
from flask import request
from flask import url_for
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """ user route.
    ---
    get:
        summary: User endpoint.
        description: Get user by ID.
        security:
            - bearerAuth: []
        parameters:
            - in: path
              name: id
              description: ID of the user
              type: integer
              required: true
        responses:
            200:
                description: User object to be returned.
                schema: UserApiSchema
                examples:
                    about_me:
                        value: "About me"
                    followed_count:
                        value: 0
                    follower_count:
                        value: 0
                    id:
                        value: 1
                    last_seen:
                        value: null
                    post_count:
                        value: 12
                    username:
                        value: "toto"
            404:
                description: User not found.
    """
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    """ User list route.
    ---
    get:
        summary: User endpoint.
        description: Get users list.
        security:
            - bearerAuth: []
        parameters:
            - in: query
              name: page
              description: The page yout want to access
              type: integer
            - in: query
              name: per_page
              description: The numbers of User to return
              type: integer
        responses:
            200:
                description: User object to be returned.
                schema: UserListApiSchema

            404:
                description: User not found.
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followers, page, per_page,
                                   'api.get_followers', id=id)
    return jsonify(data)


@bp.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followed, page, per_page,
                                   'api.get_followed', id=id)
    return jsonify(data)


@bp.route('/users', methods=['POST'])
@token_auth.login_required
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
