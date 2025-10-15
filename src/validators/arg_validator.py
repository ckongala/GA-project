class arg_validator:

    def validate_sentiment_arg(self, request):
        if 'sentiment' in request.args.keys() and request.args['sentiment'].lower() not in ['true', 'false']:
            raise Exception('sentiment argument should be bool')
