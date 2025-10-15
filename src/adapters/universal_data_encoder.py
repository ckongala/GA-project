from json import JSONEncoder


class universal_data_encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
