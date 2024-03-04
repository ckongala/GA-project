from flask import request, abort
from flask_restful import Resource
from flask_restful import current_app as app

from jsonschema import validate
from jsonschema import exceptions as json_exceptions

from models.youtube.barcode_request_schema import barcode_request_schema

from validators.auth_validator import auth_validator

from services.youtube.barcode_service import barcode_service


class barcode_controller(Resource):

    def __init__(self):


        self.validate_headers = auth_validator().validate_headers_class1
        self.barcode_service = barcode_service()

    def post(self):
        app.logger.info('Received a /youtube/generate-barcode post request')
        if not self.validate_headers(request.headers):
            abort(401, 'Invalid or No Auth-Key in request_headers')
        try:
            validate(request.json, barcode_request_schema)
        except json_exceptions.ValidationError as error:
            app.logger.error('Json request validation error: ', error)
        return self.barcode_service.generate_barcodes(request.json)
