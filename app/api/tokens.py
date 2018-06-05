from flask import g, jsonify
from app import db
from app.api import bp
from app.api.auth import basic_auth


@bp.route('/tokens', methods=["GET"])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({"token": token})


def revoke_token():
    pass
