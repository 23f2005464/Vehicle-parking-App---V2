from models import *

active = Reserve_parking_spot.query.filter_by(
            user_id=user.id,
            end_parking_timestamp=None
         ).first()

print(active)