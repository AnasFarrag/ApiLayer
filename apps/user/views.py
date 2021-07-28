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

import json


#Anas
from PIL import Image, ImageFont, ImageDraw 

from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display

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
    Updatung user info in the erp
    inputs: Erp endpoint
              All the info in the request
    output: Return Erp Response
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
        
        try:
            #post the endpoint and return the data
            response = requests.post(erp_url ,json= ERP_data, headers= headers )
            return response.json()
        except:
            return utils.message['required_fields'],400
        

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
      
    '''
    Create a certificate image of student name and the date and the course name 
    and upload the certificate to the cloud and save the link in the ERP 
    
    '''

    def post(self):
        
        #take the data from the request
        request_data = request.get_json()

        #open certficate image 
        my_image = Image.open("{}certificate_vol.jpg".format(settings.UPLOAD_DIR))
        try:
            # take some input from the request
            student_name = request_data['student_name']
            course_name = request_data['course_name']
            course_hours = request_data['course_hours']
            enrollment_id  = request_data['enrollment_id']

        except:
            return utils.message['required_fields'] , 400

        

        try:
        #reshape the input if it's arabic language for the course name
            course_name = arabic_reshaper.reshape(course_name)
            course_name = get_display(course_name)


            #reshape the input if it's arabic language for the student name
            student_name = arabic_reshaper.reshape(student_name)
            student_name = get_display(student_name)
            
            

            # time now
            now = datetime.now()
            #divide time to year, month, day, weekday
            year, month , day , day_of_week= now.strftime("%Y"),now.strftime("%m") , now.strftime("%d") , now.strftime("%A")
            #the date in the form of the certificate
            date = "{}, {} {}th, {}".format(day_of_week,month,day,year)
        

            # font type 
            font = '{}fonts/sahel.ttf'.format(settings.STATIC_DIR)
            
            # make the image into object can edit on it
            image_editable = ImageDraw.Draw(my_image)

            #write Date in certficate
            self.writeDate(image=image_editable , date=date , x= 160 , y= 400 , font_size = 35 , font_type = font)

            #write course name
            self.writeCourseName(image=image_editable , coursename=course_name , x=160, y= 640 , font_size = 35 , font_type = font)

            #write student Name 
            self.writeStudentName(image=image_editable , student_name= student_name , x=160 , y=520 , font_size=40 , font_type = font)

            #write course hours 
            self.writeCourseHours(image=image_editable , course_hours= course_hours , x=570 , y= 695 , font_size=25 , font_type = font)

            #save Image
            img = my_image.save(''.join((settings.UPLOAD_DIR , "result.jpg")))

            #open image
            img = Image.open(''.join((settings.UPLOAD_DIR , "result.jpg")))

            #make pdf file of the image
            pdf1_filename = ''.join((settings.UPLOAD_DIR , "certificate.pdf"))

            #save the pdf file 
            img.save(pdf1_filename, "PDF" ,resolution=100.0, save_all=True)

        except:
             return utils.message['error'] , 400

        try:
            if img : 
                executor = concurrent.futures.ThreadPoolExecutor()
                #image link
                image_link =  executor.submit(UserHelper.upload_file, 'result.jpg' )
                #pdf link
                pdf_link = executor.submit(UserHelper.upload_file, 'certificate.pdf' )
                #image link
                image_link = image_link.result()
                pdf_link = pdf_link.result()
                #save the image link in erp
                self.saveInErp(enrollment_id=enrollment_id , certification_image_url= image_link)

                
                # the response of 
                response = {
                  'status' : 'success',
                 'message' : 'the certifcate succefully uploaded',
                 'image_link' : image_link , 
                 'pdf_link' : pdf_link
                       } , 200

                return response

        except:
            
            response = {
            'status' : 'error',
            'message' : 'File not uploaded'
            } , 400
            return response

    
    def writeDate(self , image , date, x,y , font_size , font_type):
        title_font = ImageFont.truetype(font = font_type,size= font_size , layout_engine=ImageFont.LAYOUT_RAQM)
        return image.text((x,y), date, (0, 0, 0), font=title_font)

    def writeCourseName(self ,  image , coursename, x,y , font_size ,  font_type):

        title_font = ImageFont.truetype(font_type, font_size , layout_engine=ImageFont.LAYOUT_RAQM)
        return image.text((x,y), coursename , (0, 0, 0), font=title_font)


    def writeStudentName(self  , image , student_name, x, y , font_size ,  font_type):
        title_font = ImageFont.truetype(font_type ,font_size , layout_engine=ImageFont.LAYOUT_RAQM)
        return image.text((x,y), student_name , (0, 0, 0), font=title_font)

    def writeCourseHours(self  , image , course_hours, x,y , font_size ,  font_type):
        title_font = ImageFont.truetype( font_type ,font_size , layout_engine=ImageFont.LAYOUT_RAQM)
        return image.text((x,y), course_hours , (0, 0, 0), font=title_font)


    def saveInErp(self,enrollment_id , certification_image_url) :

        #endpoint of the certificate saved in erp
        erp_endpoint = settings.ERP_CERTIFICATE.format(enrollment_id)

         #the header
        headers = {"Authorization": settings.ERP_TOKEN ,
                    "Content-Type" : "application/json"
        }

        # the link of the image in the cloud
        erp_data = {
            'certification_image' : certification_image_url ,
        }

        
        try:
            #
            response = requests.put(erp_endpoint, json= erp_data,  headers=headers) 
            
            return response.status_code
        except Exception as e:
           
            return False




class UserInstructor(Resource):
        '''
        Description

        we give a specific person an instructor role depend on a login token from SSO

        '''
        session = FuturesSession()
        def post(self):


            try:
                #get the data from the request
                request_data = request.get_json()
                user_sub = request_data['user_sub']    
            
            except:
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
    
                    return response.json()
                    
                    

            except:
                return utils.message['error'], 400
              
               

        def loginSSO(self):
                    #total_url_SSO_instructor
                total_url = settings.SSO_LOGIN

                #data sent to url
                data = {
                        'client_id' : 'website',
                        'client_secret' : 'fe56abe3-4489-4ada-b0c6-7aa36ccd2e6d',
                        'grant_type' : 'client_credentials'
                }
                
                try:
                    #post data to url
                    response = self.session.post(total_url , data=data).result()
                    response = response.json()
                     #check access_token from the response
                    if response['access_token']:
                        return response['access_token']

                except:
                    return False




class SaveLanguage(Resource):
    '''
    save the updated language of the user
    
    '''
    
    def post(self):

        try:
            # get the data from the request
            request_data = request.get_json()

            language = request_data["language"]

            user_sub = request_data['user_sub']
        except:
            return utils.message['required_fields'] , 400

        #check params in the request
       
        instructoor = UserInstructor()
        token = instructoor.loginSSO()

        end_point = settings.USER_LANGUAGE.format(user_sub)

        #the headers of the SSO      
        headers = {
                    "Authorization": "bearer {}".format(token),
                    "Content-Type": "application/json"
                    }
        
       
        
        try:
            #get response from SSO
            res = requests.get(url=end_point , headers=headers).json() 
            #change value of language to the new one
            res['attributes']['language'] = [language]
            #update languge
        
            response = instructoor.session.put(url=end_point , json= res , headers=headers).result()
            #chech response
            if response.ok :
                return utils.message['save_language_successs'] , 200
                #return requests.get(url=end_point , headers=headers).json()
                
        except:
            return utils.message['error'] , 404

        
        return response.json() , response.status_code








