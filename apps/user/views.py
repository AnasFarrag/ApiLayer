from flask_restful import Resource
from flask import request
import json
import requests
import settings
from helpers import utils
from helpers.user.user_helpers import UserHelper

from requests_futures.sessions import FuturesSession

class UpdateUser(Resource):

    sso_sub = None
    token = None
    first_name = None
    last_name = None
    phone_number = None
    email = None
    file = None
    image_link = None
    url = None


    def post(self):

        # get request data
        request_data = request.form

        try:
            self.sso_sub = request_data['sub']
            self.token = request_data['token']
            self.first_name = request_data['given_name']
            self.last_name = request_data['family_name']
            self.phone_number = request_data['phone_number']
            self.email = request_data['email']
            self.image_link = request_data['image']
            self.url = request_data['url']
        except:
            return utils.message['required_fields'],400


        # check if SSO, ERP, and CLOUD  is running
        if not self.check_services():
            return utils.message['server_down'],503

        try:
            # get image from the request
            self.file = request.files['file']

            # Upload image to the CLOUD if exists
            self.image_link = self.upload_image()
            if self.image_link is False:
                return utils.message['image_not_valid']
        except:
            pass

        # Save data in the the ERP
        ERP_response = self.save_data_in_erp()

        if ERP_response[0] is not True:
            return ERP_response

        # save user's data in SSO
        SSO_response = self.save_data_in_sso()

        if SSO_response[0] is not True:
            return SSO_response

        return utils.message['update_user_success'], 200


    # other class functions

    # check if SSO, ERP, and CLOUD are running
    def check_services(self):
        session = FuturesSession()
        # These requests will run at the same time
        try:
            cloud = session.get(settings.CLOUD_URL)
            erp = session.get(settings.ERP_URL)
            sso = session.get(settings.SSO_BASE_URL)

            cloud_result = cloud.result()
            erp_result = erp.result()
            sso_result = sso.result()

            return True
        except:
            return False

    def upload_image(self):
        # assign image url to a variable
        self.image_link = UserHelper.upload_file(self.file, self.sso_sub)
        return self.image_link


    def save_data_in_erp(self):
        try:

            # ERP Data
            ERP_data = json.dumps({
                'url': self.url,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'student_mobile_number': self.phone_number,
                'student_email_id': self.email,
                'image': self.image_link,
            })

            # ERP Full path
            erp_url = settings.ERP_URL + self.url

            # Adding authorization token to the headers
            headers = {"Authorization": settings.ERP_TOKEN}

            # Hit ERP API and get the response
            try:
                response = requests.post(erp_url, data = ERP_data , headers = headers)

                # return response data if the resquest is not corrupted
                return (True,) if response.ok else (utils.message['error'], response.status_code)
            except:
                return utils.message['error'], response.status_code

        except:
            return utils.message['required_fields'],400



    def save_data_in_sso(self):
        try:

            # SSO Data
            SSO_data = json.dumps({
                'firstName': self.first_name,
                'lastName': self.last_name,
                'attributes': {
                    'phoneNumber': self.phone_number,
                    'image': self.image_link,
                }
            })


            # SSO Full path
            sso_url = settings.SSO_UPDATE_USER_URL.format(self.sso_sub)

            # Adding authorization token to the headers
            headers = {"Authorization": settings.SSO_TOKEN.format(self.token), "Content-Type": "application/json"}

            # Hit ERP API and get the response
            try:
                response = requests.put(sso_url, data = SSO_data , headers = headers)

                # return response data if the resquest is not corrupted
                return (True,) if response.ok else (utils.message['unauthorized'], 401)
            except:
                return utils.message['error'],500

        except:
            return utils.message['required_fields'],400



class UpdateUserInfo(Resource):

    def post(self):
        pass

class ResetPassword(Resource):

    sso_sub = None
    token = None
    password = None

    def post(self):

        # get data of comming request
        request_data = request.get_json()


        try:
            # get SSO sub
            self.sso_sub = request_data['sub']
            # get token
            self.token = request_data['token']
            # get password
            self.password = request_data['password']
        except Exception as e:
            return utils.message['required_fields'], 400

        # get SSO URL and then append SSO sub to it
        sso_url = settings.SSO_RESET_PASSWORD_URL.format(self.sso_sub)

        # Wrapp the new password in a format which SSO can understand
        sso_new_password = self.load_data()

        # Adding authorization token to the headers
        headers = {"Authorization": settings.SSO_TOKEN.format(self.token), "Content-Type": "application/json"}


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
    def load_data(self):

        data = json.dumps({
            'type': 'password',
            'value': self.password,
            'temporary': 'false',
        })

        return data


class GenerateCertificate(Resource):

    def post(self):
        pass
