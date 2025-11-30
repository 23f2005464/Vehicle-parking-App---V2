
import jwt, time
from celery_application import CeleryConfig


def get_presign_secret():
    SECRET_KEY= CeleryConfig.JWT_SECRET_KEY
    return SECRET_KEY

def create_signed_download_token(filename, expires=300):
    payload = {
        "filename": filename,
        "exp": int(time.time()) + expires
    }
    return jwt.encode(payload, get_presign_secret(), algorithm="HS256")

def verify_signed_download_token(token):
    try:
        data = jwt.decode(token,get_presign_secret(), algorithms=["HS256"])
        return data["filename"]
    except:
        return None
