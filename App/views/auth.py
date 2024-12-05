from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user as jwt_current_user, set_access_cookies
from flask_login import login_required, login_user, current_user, logout_user

from .index import index_views
from App.models import Staff, Student, User
from App.controllers import (create_user, jwt_authenticate, login)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')
'''
Page/Action Routes
'''


@auth_views.route('/users', methods=['GET'])
def get_user_page():
  users = get_all_users()
  return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
  return jsonify({
      'message':
      f"username: {current_user.username}, id : {current_user.ID}"
  })


@auth_views.route('/login', methods=['POST'])
def login_action():
  data = request.form
  message="Bad username or password"
  user = login(data['username'], data['password'])
  if user:
    user_type = type(user)
    print("User type:", user_type)
    login_user(user)
    if (user.user_type == "staff"):
      return redirect("/StaffHome")  # Redirect to student dashboard
    elif (user.user_type == "student"):
      return redirect("/StudentHome")  # Redirect to staff dashboard
    elif (user.user_type == "admin"):
      return redirect("/admin")
  return render_template('login.html', message=message)


@auth_views.route('/logout', methods=['GET'])
def logout_action():
  logout_user()
  # data = request.form
  # user = login(data['username'], data['password'])
  #return 'logged out!'
  return redirect("/")


'''
API Routes
'''


@auth_views.route('/api/users', methods=['GET'])
def get_users_action():
  users = get_all_users_json()
  return jsonify(users)


@auth_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
  data = request.json
  create_user(data['username'], data['password'])
  return jsonify({'message': f"user {data['username']} created"})



@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    token = jwt_authenticate(data['username'], data['password'])
    if not token:
        return jsonify(message='Bad username or password'), 401
    return jsonify(access_token=token), 200



@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
  return jsonify({
      'message':
      f"username: {jwt_current_user.username}, id : {jwt_current_user.ID}"
  })


@auth_views.route('/api/display_karma', methods=['GET'])
@jwt_required()
def display_karma():
    current_user_username = get_jwt_identity()  # Get username from JWT token
    print(f"JWT Identity (Username): {current_user_username}")  # Debugging line
    user = User.query.filter_by(username=current_user_username).first()

    if user is None:
        return jsonify({"message": "User not found"}), 404  # User not found

    # Log user type for debugging
    print(f"User type: {user.user_type}")  # Debugging line

    if user.user_type == "student":
        student = Student.query.filter_by(id=user.id).first()
        if student:
            return jsonify({
                "message": f"Karma Points for Student {student.full_name}",
                "karma": student.karma
            }), 200
        else:
            return jsonify({"message": "Student not found"}), 404
    else:
        return jsonify({"message": "Unauthorized. Only students can access this."}), 403
