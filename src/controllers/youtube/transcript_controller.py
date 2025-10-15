from flask import request, abort
from flask_restful import Resource
from flask_restful import current_app as app

from jsonschema import validate, exceptions

from models.youtube.transcription_request_schema import transcription_request_schema

from validators.auth_validator import auth_validator

from services.youtube.transcript_service import transcript_service
from validators.request_validator import request_validator
from constants.validation_constants import *


class transcript_controller(Resource):

    def __init__(self):
        self.validate_headers = auth_validator().validate_headers_class2
        self.transcript_service = transcript_service()
        self.validate_data_entries = request_validator().validate_data

    def post(self):
        app.logger.info('Received a /youtube/transcript get request')
        if not self.validate_headers(request.headers):
            abort(401, 'Invalid or No Auth-Key in request_headers')
        try:
            validate(request.json, transcription_request_schema)
            self.validate_data_entries(request.json, TRANSCRIPT_VALIDATION_EXPECTED_KEYS)
        except (exceptions.ValidationError, Exception)  as error:
            status_code = 400
            return (f"{error}", status_code)
        return self.transcript_service.get_video_transcripts(request.json)
