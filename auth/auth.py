from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from models.user import User  # Ensure this model is correctly defined

bcrypt = Bcrypt()
jwt = JWTManager()

def initialize_auth(app):
    bcrypt.init_app(app)
    jwt.init_app(app)

def create_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password)
    user.save()  # Make sure this method actually persists data to your database
    return user is not None

def authenticate_user(username, password):
    user = User.objects(username=username).first()  # Ensure this query is correct
    if user and bcrypt.check_password_hash(user.password, password):
        return True
    return False
