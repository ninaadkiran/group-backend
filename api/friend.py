from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.friends import Friend

# Change variable name and API name and prefix
friend_api = Blueprint('friend_api', __name__,
                   url_prefix='/api/friends')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(friend_api)

class FriendAPI:     
    class _CRUD(Resource):
        def post(self):
            
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            uidfriend = body.get('uidfriend')
            if uidfriend is None or len(uidfriend) < 2:
                print("%%%%% name error")
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                print("%%%%% name error")
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            # look for password and tokens


            print("%%%%% here1"+uid)
            ''' #1: Key code block, setup PLAYER OBJECT '''
            
            
            friend = Friend.query.filter_by(_uid=uid, _uidfriend=uidfriend).first()
            
            if friend:
                return {'message': f'Processed {uid}, either a format error or firend User ID {uidfriend} is duplicate'}, 210
            else:
                
                po = Friend(uidfriend=uidfriend, uid=uid)
                        
                print("%%%%% herdsfdse1")
                ''' #2: Key Code block to add user to database '''
                # create friend in database
                friend = po.create()
                # success returns json of friend
                
                print(jsonify(friend.read()))
                
                if friend:
                    return jsonify(friend.read())
                
                # failure returns error
                print("%%%%% herdsfdse23");
                return {'message': f'Processed {uid}, either a format error or firend User ID {uidfriend} is duplicate'}, 210
          
        def get(self,uid):
            
            if uid is None or len(uid) < 2:
                print("%%%%% name error")
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            
            friends = Friend.query.filter_by(_uid=uid).all()   # read/extract all friends from database
            json_ready = [friend.read() for friend in friends]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps


    # building RESTapi endpoint, method distinguishes action
    api.add_resource(_CRUD, '/','/<string:uid>')
