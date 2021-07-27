import os
# global class to set config variables for Flask
class Config():
    """
    Global Configurations

    """

    DEBUG = False
    SECRET_KEY = os.urandom(16)
    SESSION_COOKIE_SECURE = True
    SERVER_NAME = '10.0.0.5:5000'
    TRAP_HTTP_EXCEPTIONS = True

    # check if the uploaded image is less than the max file limit
    MAX_CONTENT_LENGTH = 10458760  #(10458760/(1024*1024)) = 10MB

    SCHEDULER_API_ENABLED = True

# class for production configurations
class production(Config):
    """
    Configurations for Production Environment
    """
    ENV = 'production'

# class for development configurations
class development(Config):
    """
    Configurations for Development Environment
    """

    DEBUG = True
    ENV = 'development'
