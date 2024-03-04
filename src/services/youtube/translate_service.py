from time import sleep
from math import ceil

from googletrans import Translator

from httpx import Timeout


class translate_service:

    def __init__(self):
        self.translator = Translator(timeout=Timeout(10.0),
                                     raise_exception=True)

    def refine_and_translate_transcripts(self, transcripts: list):
        refined_transcripts = self.refine_transcripts(transcripts)
        translated_transcripts = self.translate_transcripts(refined_transcripts)
        return translated_transcripts

    def refine_transcripts(self, transcripts: list):
        refined_transcripts = []
        for transcript_dictionary in transcripts:
            if transcript_dictionary['transcript'] is not None \
                    and transcript_dictionary['transcript'] != 'Not Video':
                refined_transcripts.append(transcript_dictionary)
        return refined_transcripts

    def translate_transcripts(self, transcripts: list):
        for i in range(len(transcripts)):
            transcripts[i]['transcript'] = \
                self.translate_transcript(transcripts[i]['transcript'])
        return transcripts

    def translate_transcript(self, transcript: str):
        transcript_chunks = self.chunk_text(transcript, 4800)
        full_translation = self.translate_transcript_chunks(transcript_chunks)
        sleep(0.1)
        translation_chunks = self.chunk_text(full_translation, 4800)
        if self.is_in_english(translation_chunks):
            return full_translation
        return 'Not English'

    def translate_transcript_chunks(self, transcript_chunks: list):
        translated_chunks = []
        for transcript_chunk in transcript_chunks:
            translated_chunks.append(self.translator.translate(transcript_chunk, dest='en').text)
            sleep(0.1)
        return ''.join(translated_chunks)

    def chunk_text(self, transcript: str, chunk_limit: int = 4800):
        transcript_chunks = []
        for i in range(ceil(len(transcript) / chunk_limit)):
            start_index = i * chunk_limit
            end_index = start_index + chunk_limit
            transcript_chunks.append(transcript[start_index:end_index])
        return transcript_chunks

    def is_in_english(self, translation_chunks: list):
        if len(translation_chunks) == 0:
            return True
        english_chunks = 0
        for translation_chunk in translation_chunks:
            chunk_language = self.translator.detect(translation_chunk)
            if chunk_language.lang == 'en':
                english_chunks += 1
        return (english_chunks / len(translation_chunks)) >= 0.8

