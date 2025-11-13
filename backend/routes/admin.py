from flask import Blueprint, request, jsonify,current_app
from flask_security import auth_required , roles_required, current_user
from db import db
from models import Parking_lots, Parking_spot
from sqlalchemy import func
admin_bp= Blueprint('admin', __name__,url_prefix='/api/admin')

@admin_bp.route('/update_profile',methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def update_profile():
    user_data=request.get_json()
    user=current_user
    if 'fullname' in user_data:
        user.fullname=user_data['fullname']
    if 'address' in user_data:    
        user.address=user_data['address']
    if 'pincode' in user_data:    
         user.pincode=user_data['pincode']
    try :
        db.session.commit()
        return jsonify({
            "message": "Profile updated successfully",
            "user": {
                "email": user.email,
                "fullname": user.fullname,
                "address": user.address,
                "pincode": user.pincode
            }
        }), 200     
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@admin_bp.route('/create_lot',methods=['POST'])
@auth_required('token')
@roles_required('admin')
def create_lot():
    lot_data=request.get_json()
    try:
        existing_lot = Parking_lots.query.filter_by(
                      prime_location=lot_data['prime_location'],
                      pincode=lot_data['pincode']).first()

        if existing_lot:
            return jsonify({"error": "A lot already exists at this location and pincode please edit a lot not create it"}), 400


        new_lot=Parking_lots(
            prime_location=lot_data['prime_location'],
            address=lot_data['address'],
            pincode=lot_data['pincode'],
            max_no_of_spots=lot_data['total_spaces'],
            price_per_hour_of_spot=lot_data['price_per_hour'],
            admin_id=current_user.id
        )
        db.session.add(new_lot)
        db.session.flush()
        #spot creation
        spot_insert=[ Parking_spot( status='A',
                lot_id=new_lot.id) for i in range(new_lot.max_no_of_spots)]
        
        db.session.bulk_save_objects(spot_insert)
        db.session.commit()

        return jsonify({
            "message": "Parking lot created successfully",
            "lot": {
                "id": new_lot.id,
                "name": new_lot.prime_location,
                "address": new_lot.address,
                "pincode": new_lot.pincode,
                "total_spaces": new_lot.max_no_of_spots,
                "price_per_hour": new_lot.price_per_hour_of_spot
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@admin_bp.route('/view_spots',methods=['GET'])
@auth_required('token') 
@roles_required('admin')    
def view_spots():
    lot_id=request.get_json().get('lot_id')
    if not lot_id:
        return jsonify({"message":"lot_id is required"}),400
    lot=Parking_lots.query.filter_by(id=lot_id,admin_id=current_user.id).first()
    if not lot:
        return jsonify({"message":"No lot found for this admin with given lot_id"}),404
    spots=Parking_spot.query.filter_by(lot_id=lot.id).all()
    spots_json=[]
    for spot in spots:
        spots_json.append({
            "spot_id":spot.id,
            "status":spot.status
        })
    return jsonify({
        "lot_id":lot.id,
        "prime_location":lot.prime_location,
        "address":lot.address,
        "pincode":lot.pincode,
        "spots":spots_json
    }),200

@admin_bp.route('/edit_lot',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def edit_lot():
    lot_data=request.get_json()
    lot_id=lot_data.get('lot_id')
    if not lot_id:
        return jsonify({"message":"lot_id is required"}),400
    lot=Parking_lots.query.filter_by(id=lot_id,admin_id=current_user.id).first()
    if not lot:
        return jsonify({"message":"No lot found for this admin with given lot_id"}),404

    if 'prime_location' in lot_data:
        lot.prime_location=lot_data['prime_location']
    if 'address' in lot_data:
        lot.address=lot_data['address']
    if 'pincode' in lot_data:
        lot.pincode=lot_data['pincode']
    if 'price_per_hour' in lot_data:
        lot.price_per_hour_of_spot=lot_data['price_per_hour']
   
    try:
        if 'total_spaces' in lot_data:
           difference=lot_data['total_spaces'] - lot.max_no_of_spots
           if difference > 0:
            # Add new spots
            spot_insert=[ Parking_spot( status='A',
                lot_id=lot.id) for i in range(difference)]
            db.session.bulk_save_objects(spot_insert)
           elif difference < 0:
            # Remove spots
            spots_to_remove = Parking_spot.query.filter_by(lot_id=lot.id, status='A').limit(-difference).all()
            if len(spots_to_remove) < -difference:
                return jsonify({"message":"Not enough available spots to remove"}),400
            for spot in spots_to_remove:
                db.session.delete(spot)
        lot.max_no_of_spots=lot_data['total_spaces']    
        db.session.commit()
        return jsonify({
            "message": "Parking lot updated successfully",
            "lot": {
                "id": lot.id,
                "name": lot.prime_location,
                "address": lot.address,
                "pincode": lot.pincode,
                "total_spaces": lot.max_no_of_spots,
                "price_per_hour": lot.price_per_hour_of_spot
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@admin_bp.route('/view_lot',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def view_lot():
    lot_id=request.get_json().get('lot_id')
    if not lot_id:
        return jsonify({"message":"lot_id is required"}),400
    lot=Parking_lots.query.filter_by(id=lot_id,admin_id=current_user.id).first()
    if not lot:
        return jsonify({"message":"No lot found for this admin with given lot_id"}),404
    spots=db.session.query(func.count(Parking_spot.id)).filter_by(lot_id=lot.id, status='A').scalar()
    lot.available_spots=spots
    return jsonify({
        "lot_id":lot.id,
        "prime_location":lot.prime_location,
        "address":lot.address,
        "pincode":lot.pincode,
        "available_spots":lot.available_spots,
        "total_spaces":lot.max_no_of_spots,
        "price_per_hour_of_spot":lot.price_per_hour_of_spot
    }),200
    
@admin_bp.route('/delete_spot',methods=['POST'])
@auth_required('token')
@roles_required('admin')
def delete_spot():
    spot_data=request.get_json()
    spot_id=spot_data.get('spot_id')
    if not spot_id:
        return jsonify({"message":"spot_id is required"}),400
    spot=Parking_spot.query.join(Parking_lots).filter(
        Parking_spot.id==spot_id,
        Parking_lots.admin_id==current_user.id
    ).first()
    if not spot:
        return jsonify({"message":"No spot found for this admin with given spot_id"}),404
    if spot.status != 'A':
        return jsonify({"message":"Only available spots can be deleted"}),400
    try:
        db.session.delete(spot)
        lot=Parking_lots.query.filter_by(id=spot.lot_id).first()
        lot.max_no_of_spots -= 1
        db.session.commit()
        return jsonify({"message":"Spot deleted successfully"}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/delete_lot',methods=['POST'])
@auth_required('token')
@roles_required('admin')
def delete_lot():
    lot_data=request.get_json()
    lot_id=lot_data.get('lot_id')
    if not lot_id:
        return jsonify({"message":"lot_id is required"}),400
    lot=Parking_lots.query.filter_by(id=lot_id,admin_id=current_user.id).first()
    if not lot:
        return jsonify({"message":"No lot found for this admin with given lot_id"}),404
    try:
        db.session.delete(lot)
        db.session.commit()
        return jsonify({"message":"Lot deleted successfully"}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500    