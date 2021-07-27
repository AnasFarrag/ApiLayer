from flask_restful import Resource
from flask import redirect
import os
import settings


# Returns nothing but a message indicates what environment application is working on
class Index(Resource):

    def get(self):
        return 'API Service is running on ' + settings.ENV + ' Environment.'

# Redirect to SSO Sign in page
class VTSRegister(Resource):

    def get(self):
        url ='https://sso.variiance.com/auth/realms/Variiance/protocol/openid-connect/registrations?client_id=reactJs&redirect_uri=https%3A%2F%2Fvts.variiance.com%2F&state=b7dbb02b-fdb5-422d-bdd7-0743830ef8f6&response_mode=fragment&response_type=code&scope=openid&nonce=fcd0d8ed-2c5c-4093-8795-54b27060af65'
        return redirect(url)
