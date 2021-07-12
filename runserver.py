
from flask import Flask
# from dotenv import load_dotenv
from urls import load_apps
from flask_restful import Api
from flask_cors import CORS
import os
import settings


def create_app(name):

    app = Flask(name)

    #set RESTFul API
    api = Api(app)

    # load installed apps
    api = load_apps(api)

    # # load .env variables
    # load_dotenv('.env')

    #set configuration environment
    app.config.from_object('config.'+ settings.ENV)

    # set CORS origin and Allowed Hosts
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

    return app

app = create_app(__name__)

if __name__ == '__main__':
    app.run()
