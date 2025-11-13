from flask import Blueprint, request, jsonify,current_app
from flask_login import login_user
from db import db
from flask_security import auth_required , roles_required, current_user
from flask_security.utils import hash_password
from werkzeug.security import check_password_hash,generate_password_hash
auth_bp = Blueprint('auth', __name__,url_prefix='/api/auth')


@auth_bp.route('/admin',methods=['GET','POST'])
@auth_required('token')
@roles_required('admin')
def admin_home():
    print("you are in admin route")
    return {"message": "Welcome to the admin dashboard!"}, 200



@auth_bp.route('/user',methods=['GET'])
@auth_required('token') 
@roles_required('user')
def user_home():
    print("user home accessed")
    user=current_user
    return {
        "email":user.email,
        "fullname":user.fullname,   
        "address":user.address,
    }

@auth_bp.route('/register',methods=['POST'])
def register():
    user_data=request.get_json()
    if not current_app.security.datastore.find_user(email=user_data['email']):
        hashed = generate_password_hash(user_data['password']) 
        current_app.security.datastore.create_user(
            email=user_data['email'],
            password=hashed,
            fullname=user_data['fullname'],
            address=user_data['address'],
            pincode=user_data['pincode'],
            roles=['user']
        )
        db.session.commit()
        return jsonify({"message":"user registered successfully"}),201
    return jsonify({"message":"user already exists"}),400
 


@auth_bp.route('/forgot_pwd',methods=['POST'])
def forgot_pwd():
    user_data=request.get_json()
    user=current_app.security.datastore.find_user(email=user_data['email'])
    if user:
        if check_password_hash(user.password,user_data['old_password']):
            new_hashed=generate_password_hash(user_data['new_password'])
            user.password=new_hashed
            try:
                db.session.commit()
                return jsonify({"message":"Password updated successfully"}),200
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500


@auth_bp.route('/login',methods=['POST'])
def login():
    print("Login route accessed")
    data=request.get_json()
    print(data)
    email=data['email']
    password=data['password']

    if not email or not password:
        return jsonify({"message":"Email and password are required"}),400
    
    user = current_app.security.datastore.find_user(email=email)
    if user :
        if check_password_hash(user.password,password):
            login_user(user)
            return jsonify({
                "id":user.id,
                "email":user.email,
                "token":user.get_auth_token()

            })
        else :
            return jsonify({"message":"Invalid password"}),400
    else :
        return jsonify({"message":"User not found"}),404   
    
