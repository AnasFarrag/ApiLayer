from flask.wrappers import Response
from requests.api import head
from flask_restful import Resource
from flask import request, jsonify
import json
import requests
import settings
from helpers import utils
from helpers.user.user_helpers import UserHelper
from requests_futures.sessions import FuturesSession
import concurrent.futures

import os , json
import demjson
from PIL import Image, ImageFont, ImageDraw
import time

class UpdateUser(Resource):

    #HINT
    # Heavey process 1-check services 2-upload image to server 3-upload image to cloud
    def post(self):

        # initialize requesrs object
        self.session = FuturesSession()
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
        if not utils.is_services_online():
            return utils.message['server_down'],503


        # Save data in the the ERP
        ERP_response = self.is_phone_number_exist()

        if ERP_response[0] is not True:
            return ERP_response


        try:
            # get image from the request
            self.file = request.files['file']

            # Upload image to the CLOUD if exists
            self.image_link = self.upload_image()
            if self.image_link is False:
                return utils.message['image_not_valid']
        except Exception as e:
            print(e)
            pass

        with concurrent.futures.ThreadPoolExecutor() as executor:

            # Save data in the the ERP
            ERP_response = executor.submit(self.save_data_in_erp)

            # save user's data in SSO
            SSO_response =  executor.submit(self.save_data_in_sso)

            ERP_response = ERP_response.result()
            SSO_response = SSO_response.result()

            if ERP_response[0] is not True:
                return ERP_response


            if SSO_response[0] is not True:
                return SSO_response

            return utils.message['update_user_success'], 200


    # other class functions

    def is_phone_number_exist(self):

        #ERP full path
        erp_url = settings.ERP_URL + settings.ERP_CHECK_PHONE_URL

        # ERP data
        ERP_data = {
            'phone': self.phone_number,
            'email': self.email
        }

        # Adding authorization token to the headers
        headers = {"Authorization": settings.ERP_TOKEN}

        # Hit ERP API and get the response
        try:
            response = self.session.post(erp_url, json = ERP_data , headers = headers)
            response = response.result()



            # return response data if the resquest is not corrupted
            return (True,) if (response.json()['status'] != 'error') else (utils.message['phone_exist'], 409)
        except Exception as e:
            print(e)
            return utils.message['error'], response.status_code


    def upload_image(self):
        #check if the uploaded file is valid image
        if not utils.is_valid_image(self.file.filename):
            return False

        #image directory
        image_dir = settings.UPLOAD_DIR + self.file.filename

        # save image to the BASE directory
        self.file.save(image_dir)

        # assign image url to a variable
        self.image_link = UserHelper.upload_file(self.file.filename)
        return self.image_link


    def save_data_in_erp(self):
        try:

            # ERP Data
            ERP_data = {
                'url': self.url,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'student_mobile_number': self.phone_number,
                'student_email_id': self.email,
                'image': self.image_link,
            }

            # ERP Full path
            erp_url = settings.ERP_URL + self.url

            # Adding authorization token to the headers
            headers = {"Authorization": settings.ERP_TOKEN}

            # Hit ERP API and get the response
            try:
                response = self.session.post(erp_url, json = ERP_data , headers = headers)
                response = response.result()
                # return response data if the resquest is not corrupted
                return (True,) if response.ok else (utils.message['error'], response.status_code)
            except:
                return utils.message['error'], response.status_code

        except:
            return utils.message['required_fields'],400



    def save_data_in_sso(self):
        try:

            # SSO Data
            SSO_data = {
                'firstName': self.first_name,
                'lastName': self.last_name,
                'attributes': {
                    'phoneNumber': self.phone_number,
                    'image': self.image_link,
                }
            }


            # SSO Full path
            sso_url = settings.SSO_UPDATE_USER_URL.format(self.sso_sub)

            # Adding authorization token to the headers
            headers = {"Authorization": settings.SSO_TOKEN.format(self.token), "Content-Type": "application/json"}

            # Hit ERP API and get the response
            try:
                response = self.session.put(sso_url, json = SSO_data , headers = headers)
                response = response.result()
                # return response data if the resquest is not corrupted
                return (True,) if response.ok else (utils.message['unauthorized'], 401)
            except:
                return utils.message['error'],500

        except:
            return utils.message['required_fields'],400



class UpdateUserInfo(Resource):

    '''
    ##Updatung user info in the erp
    ##inputs: Erp endpoint
              All the info in the request
    ##output: Return Erp Response
    '''



    def post(self):
        #get data from Request
        ERP_data = request.get_json()
        #get endpoint
        endpoint = ERP_data['url']
        #the totasl erp url
        erp_url = settings.ERP_URL + endpoint

        #the header
        headers = {"Authorization": settings.ERP_TOKEN ,
                    "Content-Type" : "application/json"
        }
        #post the endpoint and return the data

        response = requests.post(erp_url , json = ERP_data, headers= headers )
        return response.json()





        #print(hh)
        #return hh



class ResetPassword(Resource):



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
        sso_new_password = {

                'type': 'password',
                'value': self.password,
                'temporary': 'false',
        }

        # Adding authorization token to the headers
        headers = {"Authorization": settings.SSO_TOKEN.format(self.token), "Content-Type": "application/json"}


        # Hit ERP API and get the response
        try:
            response = requests.put(sso_url, json = sso_new_password , headers = headers)

            if response.ok:
                return utils.message['Reset_password_success'],200
            else:
                return utils.message['error'], response.status_code
            # return response data if the resquest is not corrupted
        except:
            return utils.message['error']



class GenerateCertificate(Resource):

    def post(self):
        pass

class UserInstructor(Resource):
        '''
        Description

        we give a specific person an instructor role
        '''
        def post(self):
            #get the data from the request
            request_data = request.get_json()

            #check user_sub
            user_sub = request_data['user_sub']
            # print(user_sub)

            if not user_sub :
                utils.message['required_fields'],404




            try:


                #url of the instructor role
                url_instructor_role = settings.SSO_INSTRUCTOR_ROLE.format(user_sub)

                #take token from loginSSO
                token = self.loginSSO()
                #take the data
                data = [{
                        "id" : "b2021e74-528b-4d7c-9012-a50b36ace032",
                        "name" : "instructors"
                    }]



                headers = {
                    "Authorization": "bearer {}".format(token),
                    "Content-Type": "application/json"
                    }


                response = requests.post(url=url_instructor_role , json = data, headers=headers)

                if response.ok :

                    return utils.message['user_instructor_successs'],200


            except:

                    return "there's someting Error!"
                #post endpoint and data

                #check telegram_id in the request

                #if true Send message to the chat_id for the instructor

                # if not return response



        def loginSSO(self):
                #total_url_SSO_instructor
                total_url = settings.SSO_LOGIN

                #data sent to url
                data = {
                        'client_id' : 'website',
                        'client_secret' : 'fe56abe3-4489-4ada-b0c6-7aa36ccd2e6d',
                        'grant_type' : 'client_credentials'
                }
                #post data to url
                response = requests.post(total_url , data=data)
                response = response.json()

                #check access_token from the response
                if response['access_token']:
                        return response['access_token']


                        #review that zzzzzzzzzzz
                return False
