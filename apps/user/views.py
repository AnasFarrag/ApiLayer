from flask.wrappers import Response
from requests.api import head
from flask_restful import Resource
from flask import request, jsonify
import json
import requests
import settings
from helpers import utils
import os , json
import demjson
class UpdateUser(Resource):
    def post(self):
        pass


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


        \

        
        
        #print(hh)
        #return hh
    
   

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
        sso_url = settings.SSO_URL.format(sso_sub)

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

                