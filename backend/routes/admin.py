from flask import Blueprint, request, jsonify,current_app
from flask_security import auth_required , roles_required, current_user
from db import db
from models import Parking_lots, Parking_spot, Reserve_parking_spot, User
from sqlalchemy import func
from datetime import timedelta,datetime,date
from cache_config import cache
admin_bp= Blueprint('admin', __name__,url_prefix='/api/admin')

def get_ist_now(time):
        parking_t= time + timedelta(hours=5, minutes=30)
        
        parking_t = parking_t.replace(tzinfo=None, microsecond=0)            #Remove timezone & microseconds
        return parking_t.strftime("%d/%m/%Y %H:%M:%S")



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
    max_spots=int(lot_data['total_spaces'])
    price_per_hour=int(lot_data['price_per_hour'])

    try:
        print("create_lot accessed")
        print(lot_data)
        existing_lot = Parking_lots.query.filter_by(
                      prime_location=lot_data['prime_location'],
                      pincode=lot_data['pincode']).first()
        print(existing_lot)
        if existing_lot:
            return jsonify({"error": "A lot already exists at this location and pincode please edit a lot not create it"}), 400


        new_lot=Parking_lots(
            prime_location=lot_data['prime_location'],
            address=lot_data['address'],
            pincode=int(lot_data['pincode']),
            max_no_of_spots=max_spots,
            price_per_hour_of_spot=price_per_hour,
            admin_id=current_user.id,
            available_spots=max_spots,  
        )
        db.session.add(new_lot)
        db.session.flush()
        #spot creation
        spot_insert=[ Parking_spot( status='A',
                lot_id=new_lot.id) for i in range(new_lot.max_no_of_spots)]
        
        db.session.bulk_save_objects(spot_insert)
        db.session.commit()
      
        cache.delete("view_lots")
        return jsonify({
            "message": "Parking lot created successfully"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@admin_bp.route('/view_spots',methods=['POST'])
@auth_required('token') 
@roles_required('admin')
def view_spots():
    lot_id=request.get_json().get('lot_id')
    print("view spots accessed")
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



@admin_bp.route('/view_spot', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def view_spot():
    req=request.get_json()
    spot_id=req.get("spot_id")
    reserve=Reserve_parking_spot.query.join(User,Reserve_parking_spot.user_id==User.id).filter(Reserve_parking_spot.spot_id ==spot_id).first()
    return jsonify({"user_id":reserve.user_id,"name":reserve.user.fullname,"email":reserve.user.email,"parking_timestamp":get_ist_now(reserve.parking_timestamp),"vehicle_number":reserve.vehicle_number})
   
   
@admin_bp.route('/search/view_user_res_info', methods=['POST'])
@auth_required('token')
@roles_required('admin')
@cache.memoize(timeout=30)
def view_user_res_info():

    # ------- same helper functions from your pay_now ----------
    def paying_hrs(hrs):
        paying_hrs = 0
        if hrs < 1:
            paying_hrs = 1
        elif hrs == int(hrs):
            paying_hrs = int(hrs)
        else:
            paying_hrs = int(hrs) + 1
        return paying_hrs

    def dr(start_time, end_time):
        hour = (end_time - start_time).total_seconds() / 3600
        nearest_int = paying_hrs(hour)
        return nearest_int

    def get_ist_now(time):
        parking_t = time + timedelta(hours=5, minutes=30)
        return parking_t.replace(tzinfo=None).replace(microsecond=0)
    # -----------------------------------------------------------

    req = request.get_json()
    user_id = req.get("user_id")
    if not user_id:
        return jsonify({"message": "user_id required"}), 400

    # fetch all reservations for this user
    reservations = Reserve_parking_spot.query.join(
        User, Reserve_parking_spot.user_id == User.id
    ).join(
        Parking_spot, Reserve_parking_spot.spot_id == Parking_spot.id
    ).join(
        Parking_lots, Parking_spot.lot_id == Parking_lots.id
    ).filter(
        Reserve_parking_spot.user_id == user_id
    ).all()

    if not reservations:
        return jsonify({"message": "No reservations found for this user"}), 404

    result = []
    current_time = datetime.utcnow()

    for reserve in reservations:
        parking_time = reserve.parking_timestamp
        duration = dr(parking_time, current_time)

        price = reserve.parking_spot.parking_lot.price_per_hour_of_spot
        amount = duration * int(price)

        result.append({
            "reservation_id": reserve.id,
            "user_id": reserve.user_id,
            "name": reserve.user.fullname,
            "email": reserve.user.email,
            "vehicle_number": reserve.vehicle_number,
            "spot_id": reserve.spot_id,
            "lot_id": reserve.parking_spot.lot_id,

            # time formatting as in pay_now
            "parking_start": get_ist_now(parking_time),
            "parking_end": get_ist_now(current_time),

            # duration + amount exactly like pay_now
            "duration": duration,
            "amount": amount
        })

    return jsonify(result), 200

      
@admin_bp.route('/edit_lot', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def edit_lot():
    lot_data = request.get_json()
    lot_id = lot_data.get('lot_id')
    if not lot_id:
        return jsonify({"message": "lot_id is required"}), 400

    lot = Parking_lots.query.filter_by(id=lot_id, admin_id=current_user.id).first()
    if not lot:
        return jsonify({"message": "No lot found for this admin with given lot_id"}), 404

    if 'prime_location' in lot_data:
        lot.prime_location = lot_data['prime_location']
    if 'address' in lot_data:
        lot.address = lot_data['address']
    if 'pincode' in lot_data:
        lot.pincode = lot_data['pincode']
    if 'price_per_hour_of_spot' in lot_data:
        lot.price_per_hour_of_spot = float(lot_data['price_per_hour_of_spot'])

    try:
        if 'total_spaces' in lot_data:
            difference = int(lot_data['total_spaces'])  - int(lot.max_no_of_spots) #edit-current

            if difference > 0:
                # Add new spots
                spot_insert = [Parking_spot(status='A', lot_id=lot.id) for i in range(difference)]
                db.session.bulk_save_objects(spot_insert)

            elif difference < 0:
                # Remove spots  
                spots_to_remove = Parking_spot.query.filter_by(lot_id=lot.id, status='A').limit(-difference).all()   #it will get the spots that is available and limit till difference 
                if len(spots_to_remove) < -difference:   #if spots to remove has spot then it is small  so  it satify <  lets see  spots available for remove 2<-(-8)             
                    return jsonify({"message": "Not enough available spots to remove"}), 400
                for spot in spots_to_remove:
                    db.session.delete(spot)

            lot.max_no_of_spots = lot_data['total_spaces']

        lot.available_spots = Parking_spot.query.filter_by(lot_id=lot.id, status='A').count()
        db.session.commit()
        cache.delete("view_lots")

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


@admin_bp.route('/view_lots',methods=['POST'])
@auth_required('token')
@roles_required('admin')
@cache.cached(timeout=120,key_prefix="view_lots")
def view_lots():
    admin_id=request.get_json().get('admin_id')
    print(admin_id)
    if not admin_id:
        return jsonify({"message":"admin_id is required"}),400
    lots=Parking_lots.query.filter_by(admin_id=admin_id).all()
    if not lots:
        return jsonify({"message":"No lot found for this admin "}),404
   
    result=[]
    for lot in lots:
      spots=db.session.query(func.count(Parking_spot.id)).filter_by(lot_id=lot.id, status='A').scalar()
      available_spots=spots
      result.append({
        "lot_id":lot.id,
        "prime_location":lot.prime_location,
        "address":lot.address,
        "pincode":lot.pincode,
        "available_spots":available_spots,
        "total_spaces":lot.max_no_of_spots,
        "price_per_hour_of_spot":lot.price_per_hour_of_spot
        })
    return jsonify(result),200





@admin_bp.route('/view_lot',methods=['POST'])
@auth_required('token')
@roles_required('admin')
def view_lot():
    admin_id=current_user
    print(admin_id,"view accessed")
    lot_id=request.get_json().get('lot_id')
    print(admin_id)
    if not admin_id:
        return jsonify({"message":"admin_id is required"}),400
    lot=Parking_lots.query.filter_by(id=lot_id,admin_id=admin_id.id).first()
    if not lot:
        return jsonify({"message":"No lot found for this admin "}),404

    return jsonify( {
        "lot_id":lot.id,
        "prime_location":lot.prime_location,
        "address":lot.address,
        "pincode":lot.pincode,
        "available_spots":lot.available_spots,
        "total_spaces":lot.max_no_of_spots,
        "price_per_hour_of_spot":lot.price_per_hour_of_spot
        }),200       
    


@admin_bp.route('/search/lot',methods=['POST'])
@auth_required('token')
@roles_required('admin')
def search_lot():
    admin_id=current_user
    print(admin_id,"view accessed")
    lot_id=request.get_json().get('lot_id')
    pincode=request.get_json().get('pincode')
    prime_location=request.get_json().get('prime_location')
    lot_json=[]
    print(admin_id)
    if not lot_id and not pincode and not prime_location:
      return jsonify({"message": "lot_id or pincode or location is required"}), 400

    if lot_id:
         lot=Parking_lots.query.filter_by(id=lot_id,admin_id=admin_id.id).first()
         if not lot:
           return jsonify({"message":"No lot found for this lot_id"}),404
         lot_json.append({
        "lot_id":lot.id,
        "prime_location":lot.prime_location,
        "address":lot.address,
        "pincode":lot.pincode,
        "available_spots":lot.available_spots,
        "total_spaces":lot.max_no_of_spots,
        "price_per_hour_of_spot":lot.price_per_hour_of_spot
        })
         
    elif pincode:
        
        lot=Parking_lots.query.filter_by(pincode=pincode,admin_id=admin_id.id).all()
        if not lot:
           return jsonify({"message":"No lot found for this pincode"}),404
     
        for l in lot:
                lot_json.append({
                "lot_id":l.id,
                "prime_location":l.prime_location,
                "address":l.address,
                "pincode":l.pincode,
                "available_spots":l.available_spots,
                "total_spaces":l.max_no_of_spots,
                "price_per_hour_of_spot":l.price_per_hour_of_spot
                })
    elif prime_location:
        print(prime_location)
        lot=Parking_lots.query.filter(Parking_lots.prime_location.ilike(f"%{prime_location}%"),Parking_lots.admin_id==admin_id.id).all()
        print(lot)
        if not lot:
           return jsonify({"message":"No lot found for this prime_location"}),404
     
        for l in lot:
                lot_json.append({
                "lot_id":l.id,
                "prime_location":l.prime_location,
                "address":l.address,
                "pincode":l.pincode,
                "available_spots":l.available_spots,
                "total_spaces":l.max_no_of_spots,
                "price_per_hour_of_spot":l.price_per_hour_of_spot
                })        
    print(lot_json)
    return jsonify(lot_json),200       





@admin_bp.route('/search/spot',methods=['POST'])
@auth_required('token')
@roles_required('admin')  
def search_spot():
    spot_id=request.get_json().get('spot_id')
    lot_id=request.get_json().get('lot_id')
    if not spot_id and not lot_id:
      return jsonify({"message": "spot_id or lot_id is required"}), 400
    spot_json=[]
    if spot_id:
            spot=Parking_spot.query.join(Parking_lots).filter(Parking_spot.id==spot_id,Parking_lots.admin_id==current_user.id).first()
            print(spot)
            if not spot:
                return jsonify({"message":"No spot found for this spot_id"}),404
            spot_json.append({
            "spot_id":spot.id,
            "status":spot.status,
            "lot_id":spot.lot_id
            })
    elif lot_id:
            spots=Parking_spot.query.join(Parking_lots).filter(Parking_spot.lot_id==lot_id,Parking_lots.admin_id==current_user.id).all()
            if not spots:
                return jsonify({"message":"No spots found for this lot_id"}),404
            for spot in spots:
                spot_json.append({
                "spot_id":spot.id,
                "status":spot.status,
                "lot_id":spot.lot_id
                })       
    return jsonify(spot_json),200

# @admin_bp.route('/reservation_info',methods=['POST'])
# @auth_required('token')
# @roles_required('admin')
# def reservation_info():
#     email=request.get_json().get('email')
#     if not email:
#         return jsonify({"message":"email is required"}),400
#     print(reservations)
   

@admin_bp.route('/search/user',methods=['POST'])
@auth_required('token')
@roles_required('admin') 
@cache.memoize(timeout=120)   
def search_user():
    user_id=request.get_json().get('user_id')
    email=request.get_json().get('email')
    fullname=request.get_json().get('name')
    print(fullname)
    if not email and not fullname and not user_id:
      return jsonify({"message": "email or fullname is required"}), 400
    user_json=[]
    if email:
            results=(db.session.query(User, func.count(Reserve_parking_spot.id).label("reservation_count")
                                      .outerjoin(Reserve_parking_spot,Reserve_parking_spot.user_id==User.id)
                                      .filter(User.email==email).group_by(User.id).all()))
            if not results:
                return jsonify({"message":"No user found for this email"}),404
            for user,reservations in results:
                if user.id==current_user.id:
                     return jsonify({"message":"This is your id"}),404
                user_json.append({
                "user_id":user.id,
                "fullname":user.fullname,
                "email":user.email,
                "address":user.address,
                "pincode":user.pincode,
                "reservations": reservations
                })
    elif fullname:
            results = (
            db.session.query(
                User,
                func.count(Reserve_parking_spot.id).label("reservation_count") )
                .outerjoin(Reserve_parking_spot, Reserve_parking_spot.user_id == User.id)
                .filter(User.fullname.ilike(f"%{fullname}%"))
                .group_by(User.id)
                .all()
    )

            if not results:
                return jsonify({"message":"No users found for this fullname"}),404
            for user,reservations in results:
                if user.id==current_user.id:
                     return jsonify({"message":"This is your id"}),404
                user_json.append({
                "user_id":user.id,
                "fullname":user.fullname,
                "email":user.email,
                "address":user.address,
                "pincode":user.pincode,
                 "reservations": reservations
                })       
    elif user_id:
            results = (
            db.session.query(
                User,
                func.count(Reserve_parking_spot.id).label("reservation_count") )
                .outerjoin(Reserve_parking_spot, Reserve_parking_spot.user_id == User.id)
                .filter(User.id==user_id)
                .group_by(User.id)
                .all()
    )

            for user,reservations in results:
                if user.id==current_user.id:
                     return jsonify({"message":"This is your id"}),404
                else:
                    user_json.append({
                    "user_id":user.id,
                    "fullname":user.fullname,
                    "email":user.email,
                    "address":user.address,
                    "pincode":user.pincode,
                    'reservations':reservations
                    })           
    return jsonify(user_json),200


@admin_bp.route('/delete_spot',methods=['DELETE'])
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
        lot=Parking_lots.query.filter_by(id=spot.lot_id).first()
        db.session.delete(spot)
        db.session.commit()  
        updated_available_spot=Parking_spot.query.filter_by(
            lot_id=lot.id, status='A'
        ).count()
        lot.available_spots=updated_available_spot
        lot.max_no_of_spots -= 1
        db.session.commit()
        cache.delete("view_lots")
        return jsonify({"message":"Spot deleted successfully"}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/delete_lot/<int:lot_id>',methods=['DELETE'])
@auth_required('token')
@roles_required('admin')
def delete_lot(lot_id):
    lot_id=int(lot_id)
    if not lot_id:
        return jsonify({"message":"lot_id is required"}),400
    lot=Parking_lots.query.filter_by(id=lot_id,admin_id=current_user.id).first()
    if not lot:
        return jsonify({"message":"No lot found for this admin with given lot_id"}),404
    is_occupied=lot.max_no_of_spots - lot.available_spots
    if is_occupied >0:
        return jsonify({"message":"Cannot delete lot with occupied spots"}),400
    try:
        db.session.delete(lot)
        db.session.commit()
        return jsonify({"message":"Lot deleted successfully"}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500    
    
@admin_bp.route('/view_users',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def view_users():
    users=User.query.all()
    
    users_json=[]
    if users is None:
        return jsonify({"message":"No users found"}),404
    else:
        for user in users:
             if user.id==current_user.id:
                continue
             users_json.append({
             "user_id":user.id,
             "fullname":user.fullname,
             "email":user.email,
             "address":user.address,
             "pincode":user.pincode,
             "active": user.is_active  
        })
        return jsonify(users_json),200
    
    
@admin_bp.route('/ban_user', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def ban_user():
    data = request.get_json()
    user_id = data.get("user_id")

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.active = False
    db.session.commit()

    return jsonify({"message": "User banned successfully"}), 200   

@admin_bp.route('/unban_user', methods=['POST'])
@auth_required('token')     
@roles_required('admin')
def unban_user():
    data = request.get_json()
    user_id = data.get("user_id")

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.active = True
    db.session.commit()

    return jsonify({"message": "User unbanned successfully"}), 200 



@admin_bp.route('/summary', methods=['GET'])
@auth_required('token')
@roles_required('admin')
@cache.cached(timeout=30)
def summary():
    admin_id = current_user.id

    # ---------------------------------------
    # admin's lots
    # ---------------------------------------
    lots = Parking_lots.query.filter_by(admin_id=admin_id).all()
    total_lots = len(lots)

    # ---------------------------------------
    # Calculating spots and gathering lot_ids
    # ---------------------------------------
    total_spots = 0
    total_available_spots = 0
    lot_ids = []

    for lot in lots:
        total_spots += lot.max_no_of_spots
        print(f"avail.spots {lot.available_spots}")
        total_available_spots += lot.available_spots
        lot_ids.append(lot.id)
    print(total_available_spots,"total avail spots")
    # ---------------------------------------
    # Reservations Count
    # ---------------------------------------
    total_reservations = Reserve_parking_spot.query.join(Parking_spot).filter(
    Parking_spot.lot_id.in_(lot_ids),  Reserve_parking_spot.end_parking_timestamp.is_(None)
).count()
    # ---------------------------------------
    # Today's revenue
    # ---------------------------------------
    today = date.today()

    today_reservations = Reserve_parking_spot.query.join(Parking_spot).filter(
    Parking_spot.lot_id.in_(lot_ids),
    db.func.date(Reserve_parking_spot.parking_timestamp) == today,
  
).all()

    print(today_reservations,"today res")
    revenue_today = sum(res.total_amount_user_paid for res in today_reservations)
    print(revenue_today,"revenue today")
    # ---------------------------------------
    # Banned Users
    # ---------------------------------------
    banned_users = User.query.filter_by(active=False).count()

    # ---------------------------------------
    # Return Summary
    # ---------------------------------------
    return jsonify({
        "total_lots": total_lots,
        "total_spots": total_spots,
        "total_available_spots": total_available_spots,
        "total_reservations": total_reservations,
        "banned_users": banned_users,
        "revenue_today": revenue_today
    }), 200
