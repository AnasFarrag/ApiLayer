from flask_restful import Resource
from flask import request
import json
import requests

class TelegramSubscription(Resource):

    def post(self):
        
    

        

        #get the data from the request
        data = request.get_json()

        # check if there's any message in the data
        if data['message']:

            chat_id = data['message']['from']['id']

            message_text = data['message']['text']
            #check message_text start with 'start'
            if 'start' in message_text:
                message = 'شكراً على انضمامك لفاريانس للإشعارات، من فضلك اكتب بريدك الإلكتروني لتفعيل الاشعارات'
                response = self.sendMessage(chat_id , message)

            elif '@' in message_text:
                response = self.saveTelegramInErp(chat_id , message_text)

                if response['status'] == 'success' :

                    message ='تم تفعيل نظام الاشعارات لك بنجاح، سوف يصلك إشعارات من قبل النظام'

                elif  response['status'] == 'error' and response['message'] == 'email not found' :

                    message ='لم يتم العثور على هذا البريد الإلكتروني لدينا، إذا كنت تريد التسجيل لدينا اضغط على اللينك التالي للتسجيل https://restapi.variiance.com/vts/register'

                else:
                    message ='لقد حدث خطأ ما أثناء تفعيل نظام الاشعارات لك، من فضلك تواصل مع قسم الدعم الفني على رقم 1002130155454 او ارسل لنا رسالة على البريد الإلكتروني support@variiance.com';


                     
                return self.sendMessage(chat_id , message)
                


    def sendMessage(self,chat_id , message):
        '''
        paass
        
        '''
        #the total telegram URL
        ### LOOK AT THE NAME OF THE mETHOD
        telegram_url = '{}/sendMessage?chat_id={}&text={}'.format(settings.TELEGRAM_URL, chat_id, message)
        #Post the message at the endpoint
        response =  requests.post(telegram_url)

        return response.json()
        

    def saveTelegramInErp(self , chat_id , email):
        
        telegram_erp_url = settings.TELEGRAM_ERP_ENDPOINT
        data = json.dumps({
            'telegram_id': chat_id,
            'email' : email
        })
        
        response = requests.post(telegram_erp_url  , data=data)

        response = response.content

        return response
        

