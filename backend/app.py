from flask import Flask,render_template # pyright: ignore[reportMissingImports]
from db import db
from flask_cors import CORS
from models import Parking_lots, User, Role
from config import Localconfig
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from routes import auth_bp,user_bp,admin_bp
from werkzeug.security import check_password_hash,generate_password_hash
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3



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
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, datastore)
    app.security = security

#-----------blueprint registration here----------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    return app

app = app_init()

@app.route('/' , methods=['POST','GET'])
def home():
    print("accessed")
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
