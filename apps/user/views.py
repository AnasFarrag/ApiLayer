from flask_restful import Resource
from flask import request
import json
import requests
import settings
from helpers import utils

class UpdateUser(Resource):
    def post(self):
        pass


class UpdateUserInfo(Resource):

    def post(self):
        pass

class ResetPassword(Resource):

    def post(self):

        # get data of comming request
        request_data = request.get_json()

        # get SSO sub
        sso_sub = request_data['sub']

        # get SSO URL and then append SSO sub to it
        sso_url = settings.SSO_URL.format(sso_sub)

        # Wrapp the new password in a format which SSO can understand
        sso_new_password = self.load_data(request_data['password'])

        # Adding authorization token to the headers
        headers = {"Authorization": settings.SSO_TOKEN.format(request_data['token']), "Content-Type": "application/json"}


        # Hit ERP API and get the response
        try:
            response = requests.put(sso_url, data = sso_new_password , headers = headers)

            if response.ok:
                return utils.message['Reset_password_success'],200
            else:
                return utils.message['error'], response.status_code
            # return response data if the resquest is not corrupted
        except:
            return utils.message['error']

    # A function, its mission is to wrapp password in a format which SSO can understand and return JSON object
    def load_data(self, password):

        data = json.dumps({
            'type': 'password',
            'value': password,
            'temporary': 'false',
        })

        return data


class GenerateCertificate(Resource):

    def post(self):
        pass
