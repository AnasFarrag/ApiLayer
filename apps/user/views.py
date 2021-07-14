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
import os , json
import demjson


#Anas
from PIL import Image, ImageFont, ImageDraw 


class UpdateUser(Resource):

    image_link = None

    def post(self):

        # get request data
        request_data = request.form

        # check if SSO, ERP, and CLOUD  is running



        try:
            # get image from the request
            image = request.files['file']


            # Upload image to the CLOUD if exists
            self.image_link = self.upload_image(image)
            if self.image_link is False:
                return utils.message['image_not_valid']
        except:
            self.image_link = request_data['image']

        # Save data in the the ERP
        ERP_response = self.save_data_in_erp(request_data)

        if ERP_response[0] is not True:
            return ERP_response

        # save user's data in SSO
        SSO_response = self.save_data_in_sso(request_data)

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

    def upload_image(self, image):
        # assign image url to a variable
        self.image_link = UserHelper.upload_file(image)
        return self.image_link

    def save_data_in_erp(self, request_data):

        try:
            # ERP endpoint
            end_point = request_data['url']

            # ERP Data
            ERP_data = json.dumps({
                'url': request_data['url'],
                'first_name': request_data['given_name'],
                'last_name': request_data['family_name'],
                'student_mobile_number': request_data['phone_number'],
                'student_email_id': request_data['email'],
                'image': self.image_link,
            })

            # ERP Full path
            erp_url = settings.ERP_URL + end_point

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


    def save_data_in_sso(self, request_data):
        try:

            # SSO Data
            SSO_data = json.dumps({
                'firstName': request_data['given_name'],
                'lastName': request_data['family_name'],
                'attributes': {
                    'phoneNumber': request_data['phone_number'],
                    'image': self.image_link,
                }
            })

            # SSO sub
            sso_sub = request_data['sub']

            # SSO token
            sso_token = request_data['token']

            # SSO Full path
            sso_url = settings.SSO_UPDATE_USER_URL.format(sso_sub)

            # Adding authorization token to the headers
            headers = {"Authorization": settings.SSO_TOKEN.format(sso_token), "Content-Type": "application/json"}

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

    '''
    ##Updatung user info in the erp 
    ##inputs: Erp endpoint
              All the info in the request
    ##output: Return Erp Response
    '''

      

    def post(self):
        #get data from Request
        data = request.get_json()
        print(data)
        #get endpoint
        endpoint = data['url']
        #the totasl erp url
        erp_url = settings.ERP_URL + endpoint
        
        ERP_data = json.dumps(data)
        print(ERP_data)
        #the header
        headers = {"Authorization": settings.ERP_TOKEN ,
                    "Content-Type" : "application/json"
        }
        #post the endpoint and return the data

        response = requests.post(erp_url ,data= ERP_data, headers= headers )
        return response.json()

class ResetPassword(Resource):

    def post(self):

        # get data of comming request
        request_data = request.get_json()

        try:
            # get SSO sub
            sso_sub = request_data['sub']

            # get token
            token = request_data['token']

            # get password
            password = request_data['password']

        except:
            return utils.message['required_fields'],404

        # get SSO URL and then append SSO sub to it
        sso_url = settings.SSO_RESET_PASSWORD_URL.format(sso_sub)

        # Wrapp the new password in a format which SSO can understand
        sso_new_password = self.load_data(password)

        # Adding authorization token to the headers
        headers = {
                    "Authorization": settings.SSO_TOKEN.format(token), 
                    "Content-Type": "application/json"
                    }


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
      
    '''
    
    '''

    def post(self):
        #take the data from the request
        request_data = request.get_json()

        my_image = Image.open("{}images/image.jpg".format(settings.STATIC_DIR))

        print(type(my_image))
        link = UserHelper.upload_file(my_image)
        print(link)

        student_name = request_data['student_name']
        course_name = request['course_name']
        course_hours = request['course_hours']
        #text = request_data['text']

        # date in interval time
        #date = 

        

        title_font = ImageFont.truetype('{}Cairo-Regular'.format(settings.STATIC_DIR),200)
        

        image_editable = ImageDraw.Draw(my_image)


        #obj.text( (x,y), Text, font, fill)
        image = image_editable.text((15,15), text, (237, 230, 211), font=title_font)
        my_image.save("result.jpg")

        return image


















class UserInstructor(Resource):
        '''
        Description

        we give a specific person an instructor role depend on a login token from SSO

        '''
        def post(self):

           
            #get the data from the request
            request_data = request.get_json()
            if not request_data : 
                return utils.message['required_fields'],404
            #check user_sub
            user_sub = request_data['user_sub']    
           

            if not user_sub or user_sub == "" : 
                return utils.message['required_fields'],404

            

               
            try:


                #url of the instructor role
                url_instructor_role = settings.SSO_INSTRUCTOR_ROLE.format(user_sub)

                #take token from loginSSO
                token = self.loginSSO()

                if token is False:
                    return utils.message['login_in_SSO_not_valid'],404
                #take the data in theat shape
                data = [{
                        "id" : "b2021e74-528b-4d7c-9012-a50b36ace032",
                        "name" : "instructors"
                    }]
                
                
                #the headers of the SSO      
                headers = {
                    "Authorization": "bearer {}".format(token),
                    "Content-Type": "application/json"
                    }
                    
                #the response 
                response = requests.post(url=url_instructor_role , json = data, headers=headers)
               
                    
                if response.ok :
                        
                    return utils.message['user_instructor_successs'],200

                elif response.status_code == 404:

                    return response.json(),404
                    
                    

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

                