from flask_restful import Resource
from flask import request
import json
import requests
import os
import owncloud

from helpers import utils
import settings

class CallApi(Resource):

    """
    CallApi is a RESTFul class which contains 4 functions POST, GET, PUT, and DELETE
    depending on requests's method type it will redirect the request to its desired function.

    """

    def post(self):
        """
        it is a function which takes ERP end point and the posted data as an input
        then post this data to the ERP.
        """

        # data of the comming request
        request_data = request.get_json()

        try:
            # ERP endpoint
            end_point = request_data['url']

            # ERP Data
            ERP_data = request_data['data']
        except:
            return utils.message['required_fields']

        # ERP Full path
        erp_url = settings.ERP_URL + end_point

        # Adding authorization token to the headers
        headers = {"Authorization": settings.ERP_TOKEN}

        # Hit ERP API and get the response
        try:
            response = requests.post(erp_url, json = ERP_data , headers = headers)

            # return response data if the resquest is not corrupted
            return response.json() if response.ok else utils.message['error'], response.status_code
        except:
            return utils.message['error']

    def get(self):

        """
        it is a function which takes ERP end point as an input
        then GET data from the ERP.
        """

        try:
            #ERP end point
            end_point = request.args.get('url')
        except:
            return utils.message['required_fields']

        # ERP full path
        erp_url = settings.ERP_URL + str(end_point)

        # Adding authorization token to the headers
        headers = {"Authorization":settings.ERP_TOKEN}

        # response must wrapped by try, except clause
        try:
            # Hit ERP API and get the response
            response = requests.get(erp_url, headers = headers)

            # return response data if the resquest is not corrupted
            return response.json() if response.ok else utils.message['error'], response.status_code
        except:
            return utils.message['error']

    def put(self):
        """
        it is a function which takes ERP end point and ERP posted data as an input
        then PUT this data to the ERP.
        """

        # data of the comming request
        request_data = request.get_json()

        try:
            # ERP endpoint
            end_point = request_data['url']

            # ERP Data
            ERP_data = request_data['data']
        except:
            return utils.message['required_fields']

        # ERP Full path
        erp_url = settings.ERP_URL + end_point

        # Adding authorization token to the headers
        headers = {"Authorization": settings.ERP_TOKEN}

        # Hit ERP API and get the response
        try:
            response = requests.put(erp_url, json = ERP_data , headers = headers)

            # return response data if the resquest is not corrupted
            return response.json() if response.ok else settings.utils['error'], response.status_code
        except:
            return settings.utils['error']

    def delete(self):
        """
        it is a function which takes ERP end point as an input
        then DETELE data from the ERP.
        """

        try:
            #ERP end point
            end_point = request.args.get('url')
        except:
            return utils.message['required_fields']

        # ERP full path
        erp_url = settings.ERP_URL + str(end_point)

        # Adding authorization token to the headers
        headers = {"Authorization":settings.ERP_TOKEN}

        # response must wrapped by try, except clause
        try:
            # Hit ERP API and get the response
            response = requests.delete(erp_url, headers = headers)

            # return response data if the resquest is not corrupted
            return response.json() if response.ok else utils.message['error'], response.status_code
        except:
            return utils.message['error']
