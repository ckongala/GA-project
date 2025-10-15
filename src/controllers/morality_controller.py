from flask import request, abort
from flask_restful import Resource
from flask_restful import current_app as app

from jsonschema import validate 

from validators.auth_validator import auth_validator

from services.morality_service import morality_service
from jsonschema import validate, exceptions
from validators.auth_validator import auth_validator

from models.morality_request_schema import morality_request_schema
from validators.request_validator import request_validator
from constants.validation_constants import *


class morality_controller(Resource):

    def __init__(self):
        super().__init__()
        self.validate_headers = auth_validator().validate_headers_class1
        self.morality_service = morality_service()
        self.validate_data_entries = request_validator().validate_data_entries

    
    def post(self):
        """
        Post Request,
        Hitting the endpoint, 
        Verifying the Auth-Key, 
        Getting the respone.   
        """ 
        app.logger.info('Received a /Morality get request')
        if not self.validate_headers(request.headers):
            abort(401, 'Invalid or No Auth-Key in request_headers')
        try:
            validate(request.json, morality_request_schema)
            self.validate_data_entries(request.json["data"], MORALITY_VALIDATION_EXPECTED_KEYS)
        except (exceptions.ValidationError, Exception) as error:
            status_code = 400
            return (f"{error}", status_code)

        data = self.morality_service.calculate_morality(request.json['data'])
        return data