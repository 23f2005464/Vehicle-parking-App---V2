from db import db
from flask import Flask
from flask_security import UserMixin, RoleMixin
from datetime import datetime

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email =db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    pincode = db.Column(db.String(7), nullable=False)
    fs_uniquifier = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True,nullable=False)
    roles=db.relationship('Role', secondary='users_and_roles', backref=db.backref('users', lazy='dynamic')) #backref is automatic way of backpopulates
    reserve_parking_spots = db.relationship('Reserve_parking_spot', backref='user', lazy='dynamic')

class Role(db.Model,RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)

class UsersAndRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

   
class Parking_lots(db.Model):
    __tablename__ = 'parking_lots'
    id = db.Column(db.Integer, primary_key=True)
    prime_location = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    pincode = db.Column(db.String(7), nullable=False)
    max_no_of_spots = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False, default=0)
    price_per_hour_of_spot = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin = db.relationship('User', backref=db.backref('parking_lots', lazy='dynamic'))

    # One-to-many relationship with Parking_spot
    parking_spots = db.relationship(
        'Parking_spot',
        backref='parking_lot',
        lazy='dynamic',
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Parking_spot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(1), nullable=False)  # 'A' or 'R'
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id', ondelete='CASCADE'), nullable=False)

    # One-to-many relationship with Reserve_parking_spot
    reservations = db.relationship(
        'Reserve_parking_spot',
        backref='parking_spot',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


class Reserve_parking_spot(db.Model):
    __tablename__ = 'reserve_parking_spot'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id', ondelete='CASCADE'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_parking_timestamp = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    total_amount_user_paid = db.Column(db.Integer, nullable=False, default=0)
    vehicle_number = db.Column(db.String(15), nullable=False)