from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from App.models import User

from datetime import timedelta
from flask_jwt_extended import create_access_token

def jwt_authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        print(f"Generating token for: {user.username}")  # Debugging line
        # Set the token to expire in 1 hour (you can adjust the expiration time as needed)
        token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
        print(f"Generated JWT Token: {token}")  # Debugging line
        return token
    return None




def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
     user = User.query.filter_by(username=identity).one_or_none()
     if user:
        return str(user.id)  # Ensure this is a string
     return None



    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt