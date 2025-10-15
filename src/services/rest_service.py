import requests

from flask_restful import current_app as app


class rest_service:

    def rest_request(self,
                     request_type: str,
                     request_url: str,
                     request_headers=None,
                     request_payload=None,
                     request_params=None):

        """
        Generic HTTP rest request method returning the HTTP Response.
        """
        response = None
        try:
            response = requests.request(method=request_type,
                                        url=request_url,
                                        headers=request_headers,
                                        data=request_payload,
                                        params=request_params)
        except requests.exceptions.RequestException as error:
            app.logger.error(error)
        return response
