class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost/koftan'
    SECRET_KEY = '378g734hg893h8jkf'
    #SECURITY_PASSWORD_SALT = 'salt'
    #SECURITY_PASSWORD_HASH = 'sha512_crypt'