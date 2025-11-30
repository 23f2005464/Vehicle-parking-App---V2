from celery import shared_task,current_task
from models import Reserve_parking_spot,Parking_spot,Parking_lots,db
import csv
import os
from datetime import timedelta
from jwt_config import create_signed_download_token
from celery_application.server_mail  import send_mail
from models import *
from weasyprint import HTML

def get_paid_res_for_multiple_users(user_ids):
       result=( db.session.query(
            Reserve_parking_spot,
            Parking_spot,
            Parking_lots,
            User
        )
        .select_from(Reserve_parking_spot)   # Force main table
        .join(User, User.id == Reserve_parking_spot.user_id)
        .join(Parking_spot, Parking_spot.id == Reserve_parking_spot.spot_id)
        .join(Parking_lots, Parking_lots.id == Parking_spot.lot_id)
        .filter(
            Reserve_parking_spot.user_id.in_(user_ids),
            Reserve_parking_spot.total_amount_user_paid != 0
        )
        .all())
       return result


def get_ist_now(time):
        parking_t= time + timedelta(hours=5, minutes=30)
        parking_t = parking_t.replace(tzinfo=None, microsecond=0)         
        return parking_t.strftime("%d/%m/%Y %H:%M:%S")
    
    
def generate_reservations_csv(reservations, filename):
    columns = [
        "id", "user_id","Full Name","Email", "vehicle_number", "spot_id",
        "lot_address", "lot_pincode",
        "start_parking_timestamp", "end_parking_timestamp",
        "duration", "Paid Amount"
    ]

    folder = "downloaded_data"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns)

        for r, s, l, u in reservations:
            writer.writerow([
                r.id,
                r.user_id,
                u.fullname,
                u.email,
                r.vehicle_number,
                r.spot_id,
                l.address,
                l.pincode,
                r.parking_timestamp,
                r.end_parking_timestamp,
                r.duration,
                r.total_amount_user_paid
            ])

    return file_path

    
    
    
@shared_task(ignore_result=False)
def reservations_csv(user_ids):
       # Handle single user
    if isinstance(user_ids, int):
        user_ids = [user_ids]

    # Single optimized query for admin (IN clause)
    res = get_paid_res_for_multiple_users(user_ids)

    # Create file
    task_id = current_task.request.id
    filename = f"res_data{task_id}.csv"

    generate_reservations_csv(res, filename)

    # Token generate
    token = create_signed_download_token(filename, expires=300)
    return token
    



@shared_task(ignore_result=True)
def user_email_reminder():
    users = User.query.all()
    print(users)
    for user in users:
        active = Reserve_parking_spot.query.filter_by(
            user_id=user.id,
            end_parking_timestamp=None
         ).all()

        if not active:
                continue  # skip if no active reservations

            # build summary text
        lines = []
        for index, res in enumerate(active, start=1):
                print(get_ist_now(res.parking_timestamp))
                lines.append(
                    f"{index}. Spot: {res.spot_id} | "
                    f"Started: {get_ist_now(res.parking_timestamp)}"
                )
        reservation_summary = "\n".join(lines)

        email_body = (
                f"Hello {user.fullname},\n\n"
                f"You currently have {len(active)} active parking reservations:\n\n"
                f"{reservation_summary}\n\n"
                "Please remember to update or end your reservation if not needed.\n"
                "Thank you!"
            )
        send_mail(
                to=user.email,
                subject="Daily Parking Reminder",
                content=email_body
            )    
        print("Email sent to →", user.email) 
    return 'sended'




@shared_task(ignore_result=False)
def user_monthly_report():
        successes = []
        failures = []
    
        users = User.query.all()
        for user in users:
            try:
                    res = Reserve_parking_spot.query.filter(
                      Reserve_parking_spot.user_id == user.id,
                        Reserve_parking_spot.end_parking_timestamp != None
                        ).all()

                    if not res:
                           raise ValueError(f"No completed reservations for user {user.id}")


                    rows = ""
                    for idx, r in enumerate(res, start=1):
                         print(r.end_parking_timestamp)
                         print(get_ist_now(r.end_parking_timestamp))
                         rows += f"""
                            <tr>
                                <td style="border:1px solid #ddd;padding:8px;">{idx}</td>
                                <td style="border:1px solid #ddd;padding:8px;">{r.spot_id}</td>
                                <td style="border:1px solid #ddd;padding:8px;">{get_ist_now(r.parking_timestamp)}</td>
                                <td style="border:1px solid #ddd;padding:8px;">{get_ist_now(r.end_parking_timestamp)}</td>
                                <td style="border:1px solid #ddd;padding:8px;">{r.total_amount_user_paid}</td>
                            </tr>
                         """
                    html_body = f"""
                    <div style="font-family:Arial,sans-serif;padding:20px;color:#333;">
                        <h2 style="color:#2B547E;">Monthly Parking Report</h2>

                        <p><strong>Hello {user.fullname},</strong></p>
                        <p>Here is your monthly parking summary:</p>

                        <table style="border-collapse:collapse;width:100%;margin-top:15px;">
                            <thead>
                                <tr style="background:#f2f2f2;">
                                    <th style="border:1px solid #ddd;padding:8px;">#</th>
                                    <th style="border:1px solid #ddd;padding:8px;">Spot ID</th>
                                    <th style="border:1px solid #ddd;padding:8px;">Start Time</th>
                                    <th style="border:1px solid #ddd;padding:8px;">End Time</th>
                                    <th style="border:1px solid #ddd;padding:8px;">Paid Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                                {rows}
                            </tbody>
                        </table>

                        <p style="margin-top:20px;">Thank you for using our service.</p>
                    </div>
                    """
                    send_mail(
                        to=user.email,
                        subject="Your Monthly Parking Report",
                        content=html_body
                    )
                    print(f"Monthly Event Sent{user.email} ")
                    return {"status": "sent", "user_id": user.id}
        
            except Exception as e:
                print(f"Error for user {user.id}: {e}")
                failures.append({"user_id": user.id, "error": str(e)})
                continue
            
        return {
        "sent": successes,
        "failed": failures,
        "sent_count": len(successes),
        "failed_count": len(failures)
        }        
 
 
 
def html_convert(res):
    user = res.user
    spot = res.parking_spot
    lot  = spot.parking_lot

        # Convert UTC naive → IST naive
    start_ist = get_ist_now(res.parking_timestamp)
    end_ist   = get_ist_now(res.end_parking_timestamp)

    html = f"""
        <div style="font-family:Arial, sans-serif; max-width:700px; margin:auto; padding:20px; border:1px solid #ddd; border-radius:10px; background:#fafafa;">
            <h2 style="text-align:center; color:#2B547E;">Parking Invoice</h2>

            <hr style="border:0; border-top:1px solid #ccc; margin:20px 0;">

            <div style="margin-bottom:20px;">
                <p style="font-size:16px; margin:5px 0;"><strong>Name:</strong> {user.fullname}</p>
                <p style="font-size:16px; margin:5px 0;"><strong>Email:</strong> {user.email}</p>
                <p style="font-size:16px; margin:5px 0;"><strong>Invoice ID:</strong> #{res.id}</p>
            </div>

            <h3 style="color:#2B547E; margin-bottom:10px;">Reservation Details</h3>

            <table style="width:100%; border-collapse:collapse; margin-bottom:20px;">
                <tr style="background:#f2f2f2;">
                    <th style="padding:10px; border:1px solid #ddd;">Field</th>
                    <th style="padding:10px; border:1px solid #ddd;">Value</th>
                </tr>

                <tr>
                    <td style="padding:10px; border:1px solid #ddd;">Spot ID</td>
                    <td style="padding:10px; border:1px solid #ddd;">{spot.id}</td>
                </tr>

                <tr>
                    <td style="padding:10px; border:1px solid #ddd;">Lot Address</td>
                    <td style="padding:10px; border:1px solid #ddd;">{lot.address}, {lot.pincode}</td>
                </tr>

                <tr>
                    <td style="padding:10px; border:1px solid #ddd;">Start Time (IST)</td>
                    <td style="padding:10px; border:1px solid #ddd;">{start_ist}</td>
                </tr>

                <tr>
                    <td style="padding:10px; border:1px solid #ddd;">End Time (IST)</td>
                    <td style="padding:10px; border:1px solid #ddd;">{end_ist}</td>
                </tr>

                <tr>
                    <td style="padding:10px; border:1px solid #ddd;">Duration (hours)</td>
                    <td style="padding:10px; border:1px solid #ddd;">{res.duration}</td>
                </tr>

                <tr>
                    <td style="padding:10px; border:1px solid #ddd;">Rate per Hour</td>
                    <td style="padding:10px; border:1px solid #ddd;">₹{lot.price_per_hour_of_spot}</td>
                </tr>

                <tr style="background:#e8f0fe;">
                    <td style="padding:10px; border:1px solid #ddd; font-weight:bold;">Total Amount Paid</td>
                    <td style="padding:10px; border:1px solid #ddd; font-weight:bold; color:green;">₹{res.total_amount_user_paid}</td>
                </tr>
            </table>

            <p style="text-align:center; margin-top:30px; font-size:14px; color:#555;">
                Thank you for using our Parking Service!
            </p>
        </div>
        """
    return html
 
 

@shared_task(ignore_result=False)
def user_invoice(res_id):
    try:
        res = (
            Reserve_parking_spot.query
                .join(User, User.id == Reserve_parking_spot.user_id)
                .join(Parking_spot, Parking_spot.id == Reserve_parking_spot.spot_id)
                .join(Parking_lots, Parking_lots.id == Parking_spot.lot_id)
                .filter(
                    Reserve_parking_spot.id == res_id,
                    Reserve_parking_spot.end_parking_timestamp != None
                )
                .first()
        )

        if not res:
            return {"error": "Reservation not found or not completed"}

        # Correct object access
        html =html_convert(res)
        filename = f"invoice_{res.id}.pdf"
        save_path = os.path.join("invoices", filename)
        HTML(string=html).write_pdf(save_path)
        
        token = create_signed_download_token(filename, expires=300)
        return token

    except Exception as e:
        return {"error": str(e)}


