class Config:
    DEBUG = False
    SECRET_KEY = 'h9idG5rsr3IGYNhWNAyY2D3TpupBb5zUF2mC'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pathology_server.db'
    HOST = "0.0.0.0"
    PORT = 5000
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXP_SECONDS = 60 * 60 * 24

    SYSTEM_USER_NAME = 'system'
    CSRF_ENABLED = True

    MAX_PATHOLOGY_PER_REQUEST = 100

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pathology_server.db'
    DEVELOPMENT = True
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 9000
    UPLOAD_FOLDER = 'D:\\flask_upload_folder'
    ALLOWED_EXTENSIONS = ['dcm', '']


class ProductionConfig(Config):
    pass