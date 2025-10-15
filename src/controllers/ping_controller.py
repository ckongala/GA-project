from flask import request, abort
from flask_restful import Resource
from flask_restful import current_app as app


class ping_controller(Resource):

    def get(self):
        """
        Get Request.
        Hitting the end point.
        To check the connection with server. 
        """
        app.logger.info('Received a ping request')
        return {
            "process name": "ETL Worker",
            "status": "working"
        }
