from flask import Flask# pyright: ignore[reportMissingImports]
from db import db
from flask_cors import CORS
from models import  User, Role,Reserve_parking_spot
from config import Localconfig
from flask_security import Security, SQLAlchemyUserDatastore
from routes import auth_bp,user_bp,admin_bp,celery_bp
from werkzeug.security import generate_password_hash
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
from cache_config import cache 
from celery_application.celery_factory import celery_init_app
import flask_excel as excel

@event.listens_for(Engine, "connect")
def sqlite_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


#forgot_password function is remaining

def app_init():
    app = Flask(__name__)
    app.config.from_object(Localconfig)
    CORS(app)
    db.init_app(app)
    
    #------------Cache init----------------------------
    cache.init_app(app) 
    
   
    
    
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, datastore)
    app.security = security

#-----------blueprint registration here----------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(celery_bp)
    return app

app = app_init()
 #-----------Celery----------------------------------
celery_app=celery_init_app(app)

excel.init_excel(app)

@app.route('/' , methods=['POST','GET'])
def home():
    
    return {"message": "Backend API running successfully"}


    
with app.app_context():
    db.create_all()
    app.security.datastore.find_or_create_role(name='admin', description='Administrator')
    app.security.datastore.find_or_create_role(name='user', description='User of the application')
    db.session.commit()
    from routes import *
    if not app.security.datastore.find_user(email="admin@gmail.com"):
        hashed = generate_password_hash("1234")
        app.security.datastore.create_user(
            email="admin@gmail.com",
            password=hashed,
            fullname="Admin User",
            address="123 Admin St",
            pincode="123456",
            roles=['admin']
        )
   
    db.session.commit()
if __name__ == '__main__':
    app.run()
