from flask import Blueprint,send_file,request,jsonify
from celery_application.tasks import reservations_csv,user_invoice
from flask_security import auth_required , roles_required,current_user
from celery.result import AsyncResult
import os
from jwt_config import verify_signed_download_token
from models import User

celery_bp=Blueprint('celery',__name__,url_prefix='/api/celery')


@celery_bp.route('/user_create_csv/<int:user_id>',methods=['GET'])
@auth_required() 
@roles_required('user')
def celery(user_id):
    task=reservations_csv.delay(user_ids=user_id)
    return {'task_id':task.id},200


@celery_bp.route('/get_data/<id>',methods=['GET'])
@auth_required() 
@roles_required('user')
def get_data(id):    
    result=AsyncResult(id)
      # Task not finished yet
    if not result.ready():
        return {"status": "pending"}, 202

    # Task failed
    if result.failed():
        return {"status": "error", "message": str(result.result)}, 500

    # Task succeeded → result should be token
    print(f"yoooooooooooo :::: {result.result}")
    return {"status": "ready", "token": result.result}, 200

@celery_bp.get("/download_csv")
def download_csv():
    token = request.args.get("token")

    filename = verify_signed_download_token(token)
    if not filename:
        return {"error": "Invalid or expired link"}, 401

    file_path = os.path.join("downloaded_data", filename)
    return send_file(file_path, as_attachment=True)     

@celery_bp.route("/invoice/<int:res_id>")
@auth_required() 
@roles_required('user')
def download_invoice(res_id):
    task = user_invoice.delay(res_id=res_id)
    return {'task_id': task.id}, 200


@celery_bp.route('/get_data_invoice/<id>')
@auth_required() 
@roles_required('user')
def get_data_invoice(id):
    result = AsyncResult(id)
    if not result.ready(): return {"status": "pending"}, 202
    if result.failed(): return {"status": "error"}, 500
    return {"status": "ready", "token": result.result}, 200

@celery_bp.route("/download_invoice")
def download_invoice_file():
    token = request.args.get("token")

    filename = verify_signed_download_token(token)
    print(filename)
    if not filename:
        return {"error": "Invalid or expired link"}, 401

    file_path = os.path.join("invoices", filename)
    print(file_path)
    return send_file(file_path, as_attachment=True)     
   
  

@celery_bp.route("/admin/download_all_reservations")
@auth_required('token')
@roles_required('admin')
def admin_download_all():
    users = User.query.all()
    user_ids = [user.id for user in users]
    task = reservations_csv.delay(user_ids)
    return jsonify({"task_id": task.id})



@celery_bp.route('/admin/user_get_data/<id>',methods=['GET'])
@auth_required('token') 
@roles_required('admin')
def users_get_data(id):    
    result=AsyncResult(id)
      # Task not finished yet
    if not result.ready():
        return {"status": "pending"}, 202

    # Task failed
    if result.failed():
        return {"status": "error", "message": str(result.result)}, 500

    # Task succeeded → result should be token
    print(f"yoooooooooooo :::: {result.result}")
    return {"status": "ready", "token": result.result}, 200


@celery_bp.get("/admin_user_download_csv")
def admin_download_csv():
    token = request.args.get("token")

    filename = verify_signed_download_token(token)
    if not filename:
        return {"error": "Invalid or expired link"}, 401

    file_path = os.path.join("downloaded_data", filename)
    return send_file(file_path, as_attachment=True) 