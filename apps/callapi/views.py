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
        image = request.files['file']

        #image directory
        image_dir = settings.UPLOAD_DIR + image.filename

        if not utils.is_valid_image(image):
            return {'message': 'File must be an image type ans less than 10MB'}
        try:
            # save image to the BASE directory
            image.save(image_dir)

            # set CLOUD URL
            oc = owncloud.Client(settings.CLOUD_URL)

            # Log In to the CLOUD
            oc.login(settings.CLOUD_USERNAME, settings.CLOUD_PASSWORD)

            # oc.mkdir('upload/123')
            oc.put_file('upload/123/123.txt', image_dir)

            link_info = oc.share_file_with_link('upload/123/123.txt')

            os.remove(image_dir)

            # we can also use
            #os.path.join(settings.BASE_DIR, str(image.filename))

        except Exception as e:
            return {'message': 'down'}

        return {'Here is your link:' :link_info.get_link() }


    def posst(self):
        """
        it is a function which takes ERP end point and the posted data as an input
        then post this data to the ERP.
        """

        # data of the comming request
        request_data = request.get_json()

        # ERP endpoint
        end_point = request_data['url']
        print(end_point)

        # ERP Data
        ERP_data = json.dumps(request_data['data'])

        # ERP Full path
        erp_url = settings.ERP_URL + end_point

        # Adding authorization token to the headers
        headers = {"Authorization": settings.ERP_TOKEN}

        # Hit ERP API and get the response
        try:
            response = requests.post(erp_url, data = ERP_data , headers = headers)

            # return response data if the resquest is not corrupted
            return response.json() if response.ok else utils.message['error'], response.status_code
        except:
            return utils.message['error']

    def get(self):

        """
        it is a function which takes ERP end point as an input
        then GET data from the ERP.
        """

        #ERP end point
        end_point = request.args.get('url')

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

        # ERP endpoint
        end_point = request_data['url']

        # ERP Data
        ERP_data = json.dumps(request_data['data'])

        # ERP Full path
        erp_url = settings.ERP_URL + end_point

        # Adding authorization token to the headers
        headers = {"Authorization": settings.ERP_TOKEN}

        # Hit ERP API and get the response
        try:
            response = requests.put(erp_url, data = ERP_data , headers = headers)

            # return response data if the resquest is not corrupted
            return response.json() if response.ok else settings.utils['error'], response.status_code
        except:
            return settings.utils['error']

    def delete(self):
        """
        it is a function which takes ERP end point as an input
        then DETELE data from the ERP.
        """

        #ERP end point
        end_point = request.args.get('url')

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
