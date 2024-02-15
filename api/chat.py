from flask import Blueprint, request, jsonify  
from flask_restful import Api, Resource 
from flask_cors import CORS
from model.chat import ChatMessage  # Import the ChatMessage model
from __init__ import app, db
import requests  

chat_api = Blueprint('chat_api', __name__, url_prefix='/api/chat')
api = Api(chat_api)
CORS(chat_api)  # Enable CORS for the chat API

class ChatAPI:
    class _Test(Resource):
        def get(self):
            response = jsonify({"Connection Test": "Successfully connected to backend!"})
            return response
        
    class _Create(Resource):
        def get(self):
            return jsonify({"message": "This is the GET request for _Create"})

        def post(self):
            data = request.json
            message = data.get('message')
            if message:
                chat_message = ChatMessage(message=message)
                db.session.add(chat_message)
                db.session.commit()
                return jsonify({"message": "Data stored successfully!"})
            else:
                return jsonify({"error": "Message is missing"}), 400

    class _Read(Resource):
        def get(self):
            chat_messages = ChatMessage.query.all()
            messages_json = [msg.serialize() for msg in chat_messages]
            return jsonify(messages_json)

api.add_resource(ChatAPI._Create, '/create')
api.add_resource(ChatAPI._Read, '/read')
api.add_resource(ChatAPI._Test, '/test')

if __name__ == "__main__":
    from app import create_app

    app = create_app()  # Create the Flask app
    app.register_blueprint(chat_api)  # Register the chat API Blueprint

    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask app
