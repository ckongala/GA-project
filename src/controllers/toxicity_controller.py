from flask import request, abort
from flask_restful import Resource
from flask_restful import current_app as app
from jsonschema import validate, exceptions

from validators.auth_validator import auth_validator
from validators.arg_validator import arg_validator

from models.toxicity_request_schema import toxicity_request_schema

from services.toxicity_service import toxicity_service
from validators.request_validator import request_validator
from constants.validation_constants import *


class toxicity_controller(Resource):

    def __init__(self):
        self.validate_headers = auth_validator().validate_headers_class1
        self.toxicity_service = toxicity_service()
        self.validate_sentiment_arg = arg_validator().validate_sentiment_arg
        self.validate_data_entries = request_validator().validate_data_entries

    def post(self):
        """
        Post Request,
        Hitting the endpoint, 
        Verifying the Auth-Key, 
        Getting the response in Json Formate.
        """
        app.logger.info('Received a /toxicity get request')
        if not self.validate_headers(request.headers):
            abort(401, 'Invalid or No Auth-Key in request_headers')
        try:
            validate(request.json, toxicity_request_schema)
            self.validate_sentiment_arg(request)
            self.validate_data_entries(request.json["data"], TOXICITY_VALIDATION_EXPECTED_KEYS)
        except (exceptions.ValidationError, Exception) as error:
            status_code = 400
            return (f"{error}", status_code)

        toxicities = self.toxicity_service.get_toxicity_scores(request.json['data'],
                                                               request.args['sentiment'].lower() == 'true')
        response = {
            "scores": toxicities
        }
        return response
