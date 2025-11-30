class Config:
  DEBUG = False
  SQL_Track_Modifications = False

class Localconfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///parking_v2.db'

  #security config 
  SECRET_KEY = 'local_dev'
 
  SECURITY_PASSWORD_HASH = 'bcrypt'
  SECURITY_PASSWORD_SALT = 'saltmixer'
  WTF_CSRF_ENABLED = False
  SECURITY_TOKEN_AUTHENTICATION_HEADER = "Token-Auth"
  SECURITY_PASSWORD_SINGLE_HASH = ['bcrypt']
  SECURITY_JSON = True
  SECURITY_API_ENABLED_METHODS = ["login"]
  HOST = '0.0.0.0'  # Allow external connections
  PORT = 5000    
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_URL = "redis://localhost:6379/0"
  CACHE_DEFAULT_TIMEOUT = 60
  