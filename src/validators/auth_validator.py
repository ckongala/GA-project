from os import environ


class auth_validator:

    def validate_headers(self, headers):
        if headers.get('Auth-Key') == environ.get('AUTH_KEY'):
            return True
        return False

    def validate_headers_class1(self, headers):
        if headers.get('Auth-Key') == environ.get('AUTH_KEY_CLASS1'): 
            return True
        return False
    
    def validate_headers_class2(self, headers):
        if headers.get('Auth-Key') == environ.get('AUTH_KEY_CLASS2'): 
            return True
        return False
    
    def validate_headers_class3(self, headers):
        if headers.get('Auth-Key') == environ.get('AUTH_KEY_CLASS3'):
            return True
        return False

