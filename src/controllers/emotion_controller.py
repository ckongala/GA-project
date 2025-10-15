from flask import request, abort
from flask_restful import Resource, current_app as app
from jsonschema import validate, exceptions
from models.emotion_request_schema import emotion_request_schema
from validators.auth_validator import auth_validator
from services.emotion_service import emotion_service
from validators.request_validator import request_validator
from constants.validation_constants import *

class emotion_controller(Resource):

    def __init__(self):
        self.validate_headers = auth_validator().validate_headers_class1
        self.emotion_service = emotion_service()
        self.validate_data_entries = request_validator().validate_data_entries

    def post(self):
        """
        POST Request,
        Receiving a JSON request,
        Validating Auth-Key,
        Handling JSON validation,
        Processing emotions,
        Sending a JSON response.
        """
        app.logger.info('Received an /emotion request')

        # Validate Auth-Key 
        if not self.validate_headers(request.headers):
            abort(401, 'Invalid or No Auth-Key in request_headers')

        try:
            validate(request.json, emotion_request_schema)
            self.validate_data_entries(request.json["data"], EMOTION_VALIDATION_EXPECTED_KEYS)    
        except (exceptions.ValidationError, Exception) as error:
            status_code = 400
            return (f"{error}", status_code)

        data = request.json.get('data', []) 
        emotions = []

        
        for item in data:
            text = item.get('text')
            emotion_scores = self.emotion_service.get_emotions(text) 
            emotion = emotion_scores[0]  # Extract the emotion label from the list
            emotions.append({
                "id": item.get("id"),
                "emotion": emotion
            })
        response = {
            "data": emotions
            
        }
        return response