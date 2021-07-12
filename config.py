import os

# global class to set config variables for Flask
class Config():
    """
    Global Configurations

    """

    DEBUG = False
    SECRET_KEY = os.urandom(16)
    SESSION_COOKIE_SECURE = True

    TRAP_HTTP_EXCEPTIONS = True

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
