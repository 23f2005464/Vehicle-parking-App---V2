import re
from models import Parking_lots, Parking_spot, Reserve_parking_spot
from flask import Blueprint, request, jsonify,current_app 
from db import db
from flask_security import auth_required , roles_required, current_user
from sqlalchemy import func
from datetime import datetime,timedelta,timezone
from sqlalchemy.exc import SQLAlchemyError
user_bp= Blueprint('user', __name__,url_prefix='/api/user')

def get_ist_now(time):
    parking_t= time + timedelta(hours=5, minutes=30)
    return parking_t.replace(tzinfo=None).replace(microsecond=0)


@user_bp.route('/profile',methods=['GET'])
@auth_required('token')
def user_profile():
    user=current_user
    return jsonify({
        "user_id":user.id,
        "email":user.email,
        "fullname":user.fullname,   
        "address":user.address,
        "pincode":user.pincode
    }),200

@user_bp.route('/update_profile',methods=['PUT'])
@auth_required('token')
@roles_required('user')
def update_profile_admin():
    user_data=request.get_json()
    user=current_user
    print(user_data)
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



@user_bp.route('/searching_lots',methods=['POST'])
@auth_required('token')
@roles_required('user') 
def searching_lots():
        search_pincode= (request.get_json() or {}).get('pincode')
        user_pincode=getattr(current_user, 'pincode', None)
        pincode_to_use=search_pincode or user_pincode
        lots=Parking_lots.query.filter_by(pincode=pincode_to_use).all() 
        print(lots)  
        if not lots:
            return jsonify({"message":"No parking lots found in your area"}),404
        
        lots_json=[]
        for lot in lots:
            spots=db.session.query(func.count(Parking_spot.id)).filter_by(lot_id=lot.id, status='A').scalar()
            lot.available_spots=spots

            lots_json.append({
                "lot_id":lot.id,
                "prime_location":lot.prime_location,
                "address":lot.address,
                "pincode":lot.pincode,
                "available_spots":lot.available_spots,  
                "price_per_hour_of_spot":lot.price_per_hour_of_spot
            })
        db.session.commit()
        return jsonify(lots_json),200        
    




@user_bp.route('/issuing_spot/preview', methods=['POST'])
@auth_required('token')
@roles_required('user')
def get_issuing_spot():
    lot_id = request.get_json()['lot_id']  # get from query params

    if not lot_id:
        return jsonify({"message": "lot_id is required"}), 400

    # Find first available spot in the given lot
    spot = Parking_spot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify({"message": "No available spots"}), 404

    # You can also fetch lot details from Parking_lot if available
    
    return jsonify({
        "message": "Spot details fetched successfully",
        "lot_info": {
            "lot_id":lot_id,
            "spot_id": spot.id,
            
        }
    }), 200


@user_bp.route('/issuing_spot',methods=['POST'])
@auth_required('token')
@roles_required('user') 
def issuing_spot():
    booking_data = request.get_json()
    lot_id = booking_data.get('lot_id')
    vehicle_number = booking_data.get('vehicle_number')

    if not lot_id or not vehicle_number:
        return jsonify({"message": "lot_id and vehicle_number are required"}), 400

    spot = Parking_spot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify({"message": "spots not available"}), 404

    issuing_spot_id = spot.id
    issue_spot_data = Reserve_parking_spot(
        user_id=current_user.id,
        spot_id=issuing_spot_id,
        parking_timestamp=func.now(),
        vehicle_number=vehicle_number
    )
    spot.status = 'R'

    try:
        db.session.add(issue_spot_data)
        db.session.commit()
        return jsonify({
            "message": "Spot reserved successfully",
            "reservation_details": {
                "reservation_id": issue_spot_data.id,
                "spot_id": issuing_spot_id,
                "lot_id": lot_id,
                "vehicle_number": vehicle_number,
                "parking_timestamp": issue_spot_data.parking_timestamp
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user_bp.route('/my_reservations', methods=['GET'])     
@auth_required('token') 
@roles_required('user')
def my_reservations():
    reservations=Reserve_parking_spot.query.join(Parking_spot,Parking_spot.id==Reserve_parking_spot.spot_id).join(Parking_lots,Parking_lots.id==Parking_spot.lot_id).filter(Reserve_parking_spot.user_id==current_user.id).all()
    print(reservations)
    if not reservations:
        return jsonify({"message":"No reservations found"}),404
    reservations_list=[]
    for res in reservations:
        reservations_list.append({
            "reservation_id":res.id,
            "spot_id":res.spot_id,
            "lot_id":res.parking_spot.lot_id,
            "parking_timestamp":res.parking_timestamp,
            "end_parking_timestamp":res.end_parking_timestamp,
            "duration":res.duration,
            "total_amount_user_paid":res.total_amount_user_paid,
            "vehicle_number":res.vehicle_number,
            "prime_location":res.parking_spot.parking_lot.prime_location,
            "address":res.parking_spot.parking_lot.address
        })
    return jsonify(reservations_list),200

@user_bp.route('/cancel_reservation', methods=['DELETE'])
@auth_required('token')
@roles_required('user') 
def cancel_reservation():
    data=request.get_json()
    reservation_id=data.get('reservation_id')
    reservation=Reserve_parking_spot.query.filter_by(id=reservation_id,user_id=current_user.id).first()
    if not reservation:
        return jsonify({"message":"Reservation not found"}),404
    spot=Parking_spot.query.filter_by(id=reservation.spot_id).first()
    spot.status='A' #making spot available again
    try:
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({"message":"Reservation cancelled successfully"}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


    


@user_bp.route('pay_now',methods=['GET','POST'])
@auth_required('token')
@roles_required('user') 
def pay_now():
    def paying_hrs(hrs):
        paying_hrs=0
        if hrs < 1:
            paying_hrs = 1
        elif hrs == int(hrs):
           paying_hrs = int(hrs)
        else:
            paying_hrs = int(hrs) + 1  #for 1.56  int(1.56) = 1 something
        return paying_hrs    

    def dr(start_time, end_time):
             hour= (end_time - start_time).total_seconds() / 3600
             nearest_int=paying_hrs(hour)
             return  nearest_int# minutes
    
           
    def get_ist_now(time):
        parking_t= time + timedelta(hours=5, minutes=30)
        return parking_t.replace(tzinfo=None).replace(microsecond=0)
  

    if request.method=='POST':
        print("payment accessed")
        data=request.get_json()
        print(data)
        
        res_id=data['reservation_id']
        current_time = datetime.utcnow()
        reservation=Reserve_parking_spot.query.join(Parking_spot).join(Parking_lots).filter(Reserve_parking_spot.id==res_id).first()
        parking_time=reservation.parking_timestamp
        dr_result=dr(parking_time,current_time)
        amt=int(dr_result)*int(reservation.parking_spot.parking_lot.price_per_hour_of_spot)
        print(amt)
        return jsonify({
            "reservation_id":res_id,
            "fullname":current_user.fullname,
            "email":current_user.email,
            "duration":dr_result,
            "amount":amt,
            "parking_start":get_ist_now(parking_time),
            "parking_end":get_ist_now(current_time)
        }),200
        #remaining watch video 

@user_bp.route('paying_transaction',methods=['POST'])
@auth_required('token')
@roles_required('user') 
def paying_transaction():
  
  try:
    data=request.get_json()
    required_fields = ['reservation_id', 'amount_user_paid', 'parking_end', 'duration']
    
    missing = [f for f in required_fields if f not in data]
    if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    res_id=data['reservation_id']
    total_amount_user_paid=data['amount_user_paid']
    parking_end=data['parking_end']
    duration=data['duration']
 
    try:
            end_parking_timestamp = datetime.fromisoformat(parking_end)
    except ValueError:
            return jsonify({"error": "Invalid datetime format for 'parking_end'"}), 400
    
   
    res=Reserve_parking_spot.query.filter_by(id=res_id).first()
   
    res.total_amount_user_paid=total_amount_user_paid
    res.end_parking_timestamp=end_parking_timestamp
    res.duration=duration
    db.session.commit()
    
    return jsonify({"message":"successfully paid"}),200
  
  except SQLAlchemyError as e:
        
        db.session.rollback()
        return jsonify({"error": "Internal server error ", "details": str(e)}), 500

  except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@user_bp.route('/user_summary', methods=['GET'])
@auth_required('token')
@roles_required('user')
def user_summary():
    print("log :: user summary initialized")
    user_id = current_user.id

    def HrsFunc(hrs):
        if hrs < 1:
            return 1
        elif hrs == int(hrs):
            return int(hrs)
        else:
            return int(hrs) + 1

    def dr(start_time, end_time):
        start_time = start_time.replace(tzinfo=timezone.utc)
        end_time = end_time.replace(tzinfo=timezone.utc)
        hour = (end_time - start_time).total_seconds() / 3600
        return HrsFunc(hour)

    # main query (keep your preferred join format)
    reservations = (
        Reserve_parking_spot.query
        .join(Parking_spot)
        .join(Parking_lots)
        .filter(
            Reserve_parking_spot.user_id == user_id,
            Reserve_parking_spot.end_parking_timestamp == None
        )
        .all()
    )

    current_timestamp = datetime.now(timezone.utc)
    summary = []
    count_loc = {}
    aggregated_durations = {}

    for res in reservations:
        parking_lot = res.parking_spot.parking_lot
        parking_spot = res.parking_spot

        start_time = res.parking_timestamp
        duration_hours = dr(start_time=start_time, end_time=current_timestamp)

        prime_loc = parking_lot.prime_location

        # Count how many active spots per location
        count_loc[prime_loc] = count_loc.get(prime_loc, 0) + 1

        # Sum total duration per location
        aggregated_durations[prime_loc] = aggregated_durations.get(prime_loc, 0) + duration_hours

        summary.append({
            "spot_id": parking_spot.id,
            "lot_id": parking_lot.id,
            "prime_location": prime_loc,
            "duration_hours": duration_hours
        })

    # convert aggregated_durations to list for bar chart
    data = [
        {"prime_location": loc, "total_duration": total}
        for loc, total in aggregated_durations.items()
    ]

    response = {
        "data": data,
        "count_loc": count_loc,
        "user_data": {"user_id": user_id}
    }

    return jsonify(response), 200

