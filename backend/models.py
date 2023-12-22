import datetime as dt
import sqlalchemy as sql
import passlib.hash as hash
import database as database  # Your database configuration or import Base from SQLAlchemy
import uuid

class User(database.Base):
    __tablename__ = "users"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    first_name = sql.Column(sql.String)  
    last_name = sql.Column(sql.String)  
    hashed_password = sql.Column(sql.String)
    date_created = sql.Column(sql.DateTime, default=dt.datetime.utcnow)
    profile_picture = sql.Column(sql.String)  # Adjust the type as needed
    
    # Relationship with Conversation (one user can have multiple conversations)
    conversations = sql.orm.relationship("Conversation", back_populates="user")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)

    def __repr__(self) -> str:
        return f"User Record {self.first_name} {self.last_name}"

class Conversation(database.Base):
    __tablename__ = "conversations"

    id = sql.Column(sql.String, primary_key=True, default=str(uuid.uuid4()))
    title = sql.Column(sql.String, nullable=False)  # Title of the conversation

    # Relationship with User (many conversations belong to one user)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"), nullable=False)
    user = sql.orm.relationship("User", back_populates="conversations")
    date_created = sql.Column(sql.DateTime, default=dt.datetime.utcnow)

    messages = sql.orm.relationship("Message", back_populates="conversation")

    def __repr__(self) -> str:
        return f"Conversation: {self.title}"



class Message(database.Base):
    __tablename__ = "messages"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    text_content = sql.Column(sql.String)  # Content of the message

    # Relationship with User (each message has an author)
    author_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"), nullable=True)
    author = sql.orm.relationship("User")
    is_bot_message = sql.Column(sql.Boolean, default=False)


    
    conversation_id = sql.Column(sql.Integer, sql.ForeignKey("conversations.id"), )
    conversation = sql.orm.relationship("Conversation", back_populates="messages")

    def __repr__(self) -> str:
        return f"Message: {self.text}"

