from __init__ import db  # Import db from the initialization file

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Establish a relationship with the User model

    user = db.relationship('User', backref=db.backref('messages', lazy=True))  # Define a relationship with the User model

    def __repr__(self):
        return f"ChatMessage(id={self.id}, message={self.message}, timestamp={self.timestamp}, user_id={self.user_id})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(e)
            return None

    @staticmethod
    def get_all_messages():
        return ChatMessage.query.all()

    def serialize(self):
        return {
            'id': self.id,
            'message': self.message,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id
        }
