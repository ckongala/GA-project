from flask import request, abort
from flask_restful import Resource
from flask_restful import current_app as app

from jsonschema import validate
from jsonschema import exceptions

from models.youtube.gpt3_keywords_request_schema import gpt3_keywords_request_schema

from validators.auth_validator import auth_validator

from services.youtube.gpt3_keywords_service import gpt3_keywords_service
from validators.request_validator import request_validator
from constants.validation_constants import *


class gpt3_keywords_controller(Resource):

    def __init__(self):
        self.validate_headers = auth_validator().validate_headers_class2
        self.gpt3_keywords_service = gpt3_keywords_service()
        self.validate_data_entries = request_validator().validate_data

    def post(self):
        app.logger.info('received /youtube/gpt3_keywords request')
        if not self.validate_headers(request.headers):
            abort(401, 'Invalid or No Auth-Key in request_headers')
        try:
            validate(request.json, gpt3_keywords_request_schema)
            self.validate_data_entries(request.json, GPT3_NARRATIVE_KEYWORDS_EXPECTED_KEYS)
        except (exceptions.ValidationError, Exception)  as error:
            status_code = 400
            return (f"{error}", status_code)
        return self.gpt3_keywords_service.get_keywords(request.json)
