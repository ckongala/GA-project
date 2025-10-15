from math import ceil

from flask_restful import current_app as app


class chunking_service:

    def __init__(self):
        self.chunk_word_limit = 800
        pass

    def get_transcript_chunk_sets(self, json_request):
        request_word_limit = json_request['chunk_word_limit']
        if request_word_limit is not None \
                and request_word_limit != 0:
            self.chunk_word_limit = request_word_limit
        app.logger.info('Chunking %d transcripts, each with chunk_word_limit: %d',
                        len(json_request['transcripts']),
                        json_request['chunk_word_limit'])
        transcript_chunk_sets = []
        for transcript in json_request['transcripts']:
            transcript_chunk_sets.append(self.get_transcript_chunks(transcript))
        return {
            'transcript_chunk_sets': transcript_chunk_sets
        }

    def get_transcript_chunks(self, transcript: str):
        words = transcript.split()
        chunks = []
        chunks_count = ceil(len(words) / self.chunk_word_limit)
        for i in range(0, chunks_count):
            if i == chunks_count - 1:
                chunks.append(' '.join(words[i*self.chunk_word_limit:]))
            else:
                chunks.append(' '.join(words[i*self.chunk_word_limit:(i+1)*self.chunk_word_limit]))
        return chunks




