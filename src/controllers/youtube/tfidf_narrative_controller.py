from flask import request, abort
from flask_restful import Resource
from flask_restful import current_app as app

from jsonschema import validate
from jsonschema import exceptions

from models.youtube.tfidf_narrative_request_schema import tfidf_narrative_request_schema

from validators.auth_validator import auth_validator

from services.youtube.tfidf_narrative_service import tfidf_narrative_service
from validators.request_validator import request_validator
from constants.validation_constants import *


class tfidf_narrative_controller(Resource):

    def __init__(self):
        self.validate_headers = auth_validator().validate_headers_class1
        self.tfidf_narrative_service = tfidf_narrative_service()
        self.validate_data_entries = request_validator().validate_data

    def post(self):
        app.logger.info('Received a /youtube/tfidf-narrative get request')
        if not self.validate_headers(request.headers):
            abort(401, 'Invalid or No Auth-Key in request_headers')
        try:
            validate(request.json, tfidf_narrative_request_schema)
            self.validate_data_entries(request.json, TFIDF_VALIDATION_EXPECTED_KEYS)
        except (exceptions.ValidationError, Exception)  as error:
            status_code = 400
            return (f"{error}", status_code)
        return self.tfidf_narrative_service.generate_tfidf_narratives(request.json)
