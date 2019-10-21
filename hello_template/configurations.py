from os import environ
import redis
class BaseConfig(object):
 '''
 Base config class
 '''
 DEBUG = True
 TESTING = False
class ProductionConfig(BaseConfig):
 """
 Production specific config
 """
 DEBUG = False
class DevelopmentConfig(BaseConfig):
 """
 Development environment specific configuration
 """
 DEBUG = True
 TESTING = True
 SECRET_KEY = 'mY sUpEr sEcReT kEy'
 secret_key = 'mY sUpEr sEcReT kEy'
 SESSION_TYPE = 'filesystem'
 #SESSION_REDIS = 'redis://:[password]@[host_url]:[port]'
 #SESSION_REDIS = 'filesystem'
 SECRET_KEY = environ.get('SECRET_KEY')
 FLASK_APP = environ.get('FLASK_APP')
 FLASK_ENV = environ.get('FLASK_ENV')

 # Flask-Session
 #SESSION_TYPE = environ.get('SESSION_TYPE')
 #SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))