
toxicity_request_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "types": "object",
                "properties": {
                    "id": {
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