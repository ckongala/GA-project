chunking_request_schema = {
    "type": "object",
    "properties": {
        "chunk_word_limit": {
            "type": "integer"
        },
        "transcripts": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
}
