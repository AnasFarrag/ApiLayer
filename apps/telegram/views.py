from flask_restful import Resource
from flask import request
import json
import requests
import settings
from helpers.telegram.telegram_helpers import TelegramHelper 
from helpers import utils

class TelegramSubscription(Resource):

    def post(self):
        #get the data from the request
        data = request.get_json()

        # check if there's any message in the data
        try:

            chat_id = data['message']['from']['id']

            message_text = data['message']['text']
           
            #check message_text start with 'start'
            if  message_text == 'start' or  message_text == 'Start'  or message_text == 'START' :
                
                message = 'شكراً على انضمامك لفاريانس للإشعارات، من فضلك اكتب بريدك الإلكتروني لتفعيل الاشعارات'
                response = self.sendMessage(chat_id , message)
                #return response

            # check for validating email
            elif  TelegramHelper.valid_email(self , message_text):
                
                #check on the email in erp
                response = self.saveTelegramInErp(chat_id= chat_id , email = message_text)
                
                # if email exists 
                if response['status'] == 'success' :

                    message ='تم تفعيل نظام الاشعارات لك بنجاح، سوف يصلك إشعارات من قبل النظام'
                # if email not exists
                elif  response['status'] == 'error' and response['message'] == 'email not found' :

                    message ='لم يتم العثور على هذا البريد الإلكتروني لدينا، إذا كنت تريد التسجيل لدينا اضغط على اللينك التالي للتسجيل https://restapi.variiance.com/vts/register'
                
                else:
                    message ='لقد حدث خطأ ما أثناء تفعيل نظام الاشعارات لك، من فضلك تواصل مع قسم الدعم الفني على رقم 1002130155454 او ارسل لنا رسالة على البريد الإلكتروني support@variiance.com';

            # if email is not valid
            else:
                message =  "يرجي كتابه البريد الالكتروني بطريقه صحيحه"

            self.sendMessage(chat_id , message)
            
        except:
             return utils.message['error']
        

    def sendMessage(self,chat_id , message):
        '''
        send message for the user Replaying to the user
        
        '''
        try:
        #token of telegram url
            token = settings.TELEGRAM_token
            #the total telegram URL
            telegram_url = '{}{}/sendMessage?chat_id={}&text={}'.format(settings.TELEGRAM_URL, token , chat_id, message)
            
            #Post the message at the endpoint
            response =  requests.post(telegram_url)
            return response.json()
        
        except: 
            return False


    def saveTelegramInErp(self , chat_id , email):
        
        try:
            telegram_erp_url = settings.TELEGRAM_ERP_ENDPOINT
            
            # data for save the email in erp
            data ={
                'telegram_id': chat_id,
                'email' : email
            }

            headers = {"Authorization": settings.ERP_TOKEN ,
                    "Content-Type" : "application/json"}
            
            # for sending data
            response = requests.post(telegram_erp_url  , json = data , headers= headers)
            
            response = response.json()
           
            return response
            
        except :
            return False



