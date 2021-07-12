from flask_restful import Resource, Api, reqparse
from flask import request, jsonify
import json
import requests
from helpers import utils
import settings
class Fawry(Resource):
    """
    It is a web hook that is used by Fawry service
    """

    def post(self):

        pass
