from os.path import abspath, join, dirname

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint

import json
import logging


from dotenv import load_dotenv

from controllers.ping_controller import ping_controller
from controllers.toxicity_controller import toxicity_controller
from controllers.twitter.botscore_controller import botscore_controller
from controllers.morality_controller import morality_controller
from controllers.youtube.transcript_controller import transcript_controller
from controllers.youtube.gpt3_keywords_controller import gpt3_keywords_controller
from controllers.youtube.gpt3_narrative_controller import gpt3_narrative_controller
from controllers.youtube.chunking_controller import chunking_controller
from controllers.youtube.tfidf_narrative_controller import tfidf_narrative_controller

from controllers.emotion_controller import emotion_controller

from controllers.youtube.barcode_controller import barcode_controller

from adapters.statsd_adapter import setting_statsd, StatsdMiddleware



env_path = abspath(join(dirname(__file__), '..', '.env'))

load_dotenv(env_path, verbose=True)

app = Flask(__name__)
api = Api(app)

setting_statsd()

app.wsgi_app = StatsdMiddleware(app.wsgi_app, "etl-worker")

app.logger.setLevel(logging.INFO)

api.add_resource(ping_controller, '/api/v1/ping/', endpoint='ping')
api.add_resource(toxicity_controller, '/api/v1/toxicity/', endpoint='toxicity')
api.add_resource(morality_controller, '/api/v1/morality/', endpoint='morality')
api.add_resource(transcript_controller, '/api/v1/youtube/transcript/', endpoint='youtube/transcript')
api.add_resource(gpt3_narrative_controller, '/api/v1/youtube/gpt3_narrative/', endpoint='youtube/gpt3_narrative')
api.add_resource(gpt3_keywords_controller, '/api/v1/youtube/gpt3_keywords/', endpoint='youtube/gpt3_keywords')
api.add_resource(chunking_controller, '/api/v1/youtube/chunk-transcripts/', endpoint='youtube/chunk-transcripts')
api.add_resource(tfidf_narrative_controller, '/api/v1/youtube/tfidf-narrative/', endpoint='youtube/tfidf-narrative')

api.add_resource(emotion_controller, '/api/v1/emotion/', endpoint='emotion')
api.add_resource(barcode_controller, '/api/v1/youtube/generate-barcode', endpoint='youtube/generate-barcode')

# Configure swagger ui
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "ETL-Worker"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

