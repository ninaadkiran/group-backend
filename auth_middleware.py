from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from model.users import User

def token_required(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # print("TOPOOPOP")
            
            token = request.cookies.get("jwt")
            # print("MOOMOM")

            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            try:
                # print("MEMEMAM")
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                current_user = User.query.filter_by(_uid=data["_uid"]).first()
                if current_user is None:
                    return {
                        "message": "Invalid Authentication token!",
                        "data": None,
                        "error": "Unauthorized"
                    }, 401

                # print("LOOOOOOOOO")
                # Check if roles are provided and user has the required role
                # print(f"FOLES:: {roles}")
                if roles and current_user.role not in roles:
                    return {
                        "message": "Insufficient permissions. Required roles: {}".format(roles),
                        "data": None,
                        "error": "Forbidden"
                    }, 403

            except Exception as e:
                # print(f"EEEEEEEE {e}")

                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e)
                }, 500

            return f(current_user, *args, **kwargs)

        return decorated
    return decorator