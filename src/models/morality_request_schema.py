
morality_request_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "types": "object",
                "properties": {
                    "url": {
                        "type": "string"
                    }, 
                    "text": {
                        "type": "string"
                    }
                }
            }
        }
    }
}