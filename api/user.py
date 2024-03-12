import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented

        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()

            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')

            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400

            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            password = body.get('password')
            dob = body.get('dob')
            color = body.get('color')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, 
                      uid=uid)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be yyy-mm-dd'}, 400
            
            ''' #2: Key Code block to add user to database '''

            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        @token_required(roles=[])
        def get(self, current_user): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
        @token_required(roles=["Admin"])
        def delete(self, current_user):
            body = request.get_json()
            uid = body.get('uid')
            users = User.query.all()
            for user in users:
                if user.uid == uid:
                    user.delete()
            return jsonify(user.read())
        
        @token_required(roles=["Admin"])
        def put(self, current_user):
            body = request.get_json() # get the body of the request
            uid = body.get('uid') # get the UID (Know what to reference)
            name = body.get('name') # get name (to change)
            password = body.get('password') # get password (to change)
            color = body.get('color') # get color (to change)
            role = body.get('role')  # get role (to change)
            users = User.query.all() # get users
            for user in users:
                if user.uid == uid: # find user with matching uid
                    user.update(name,'',password,color, role) # update info
            return f"{user.read()} Updated"
        
    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')

                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')

                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400

                if user:
                    print("GOT USER")
                    try:
                        token_payload = {
                            "_uid": user._uid,
                            "role": user._role  # Add the role information to the token
                        }
                        print(f"token_payload={token_payload}")
                        token = jwt.encode(
                            token_payload,
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        print("after token")
                        resp = Response("Authentication for %s successful" % (user._uid))
                        print(f"after response: {token}")
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None',  # This is the key part for cross-site requests
                                # domain="0.0.0.0"
                                )
                        print(f"after set_cookie: resp={resp}")
                        print(f"after set_cookie: resp.headers={resp.headers}")
                        # print(dir(resp))
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 501
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                print(f"Got exception: {e}")
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 502

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')