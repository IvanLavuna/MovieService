from movie_app.models import db_session
from flask_httpauth import HTTPBasicAuth
from movie_app.models import User
from flask import g
from functools import wraps

session = db_session()

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.user.role not in roles:
                return "You are not authorized to access this page\n"
            return f(*args, **kwargs)
        return wrapped
    return wrapper
