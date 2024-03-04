from flask import request, abort
from flask_restful import Resource
from flask_restful import current_app as app

from jsonschema import validate
from jsonschema import exceptions

from models.youtube.chunking_request_schema import chunking_request_schema

from validators.auth_validator import auth_validator

from services.youtube.chunking_service import chunking_service
from validators.request_validator import request_validator
from constants.validation_constants import *


class chunking_controller(Resource):

    def __init__(self):
        self.validate_headers = auth_validator().validate_headers_class1
        self.chunking_service = chunking_service()
        self.validate_data_entries = request_validator().validate_data

    def post(self):
        app.logger.info('Received a /youtube/chunk-transcripts get request')
        if not self.validate_headers(request.headers):
            abort(401, 'Invalid or No Auth-Key in request_headers')
        try:
            validate(request.json, chunking_request_schema)
            self.validate_data_entries(request.json, TRANSCRIPT_CHUNKS_EXPECTED_KEYS, is_chunk=True)
        except (exceptions.ValidationError, Exception)  as error:
            status_code = 400
            return (f"{error}", status_code)
        return self.chunking_service.get_transcript_chunk_sets(request.json)
