from flask_restful import Resource, Api, reqparse
from flask import request, jsonify
import json
import requests
from helpers import utils
import settings
class Fawry(Resource):
    """
    It is a web hook that is used by Fawry service
    """

    def post(self):

        # data of fawry request
        request_data = request.get_json()

        # Fawry end point
        fawry_erp_end_point = settings.FAWRY_ERP_END_POINT

        # ERP Full path
        erp_url = settings.ERP_URL + fawry_erp_end_point

        # ERP Data
        ERP_data = json.dumps(request_data)
        print(ERP_data)

        # Adding authorization token to the headers
        headers = {"Authorization": settings.ERP_TOKEN}

        # Hit ERP API and get the response
        try:
            response = requests.post(erp_url, data = ERP_data , headers = headers)

            # TODO No return response
            # return response data if the resquest is not corrupted
            return response.json() if response.ok else utils.message['error'], response.status_code
        except:
            return utils.message['error']
