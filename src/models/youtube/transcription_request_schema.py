
transcription_request_schema = {
    "type": "object",
    "properties": {
        "video_ids": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "tracker_ids": {
            "type": "array",
            "items": {
                "type": "integer"
            }
        }
    }
}
