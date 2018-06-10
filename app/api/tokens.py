from flask import g, jsonify
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route('/tokens', methods=["GET"])
@basic_auth.login_required
def get_token():
    """ Retrieve token route.
    ---
    get:
        summary: User followed endpoint.
        description: Get followed list.
        security:
            - basicAuth: []
        responses:
            200:
                description: Token to use for other api route
                schema: TokenApiSchema

            404:
                description: User not found.
    """
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({"token": token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
