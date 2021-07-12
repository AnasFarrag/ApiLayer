from flask_restful import Resource
from flask import redirect
import os
import settings


# Returns nothing but a message indicates what environment application is working on
class Index(Resource):

    def get(self):
        pass

# Redirect to SSO Sign in page
class VTSRegister(Resource):

    def get(self):
        pass
