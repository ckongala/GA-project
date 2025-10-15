from os import environ

import openai
from openai import ErrorObject as openai_error

from flask_restful import current_app as app


class gpt3_narrative_service:

    def __init__(self):
        openai.api_key = environ.get('OPENAI_API_KEY')
        self.engine = "davinci-instruct-beta-v3"
        self.temperature = 0
        self.max_tokens = 25
        self.top_p = 1
        self.frequency_penalty = 0
        self.presence_penalty = 0

    def get_narratives(self, request_json):
        chunks = request_json['chunks']
        app.logger.info('Requesting GPT3 for narratives for %d transcripts', len(chunks))
        narratives = []
        for chunk in chunks:
            narratives.append(self.get_narrative_from_text(chunk))
        return {
            'narratives': narratives
        }

    def get_narrative_from_text(self, text: str):
        narrative = None
        try:
            openai_response = openai.Completion.create(
                engine=self.engine,
                prompt=self.get_narrative_prompt(text),
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )
            narrative = openai_response.choices[0].text
        except openai_error:
            app.logger.info('OpenAI Exception occurred, Exception: ', openai_error)
        except Exception as error:
            app.logger.info('Exception occurred while getting keywords from gpt3, Exception: ', error)
        return narrative.replace("\n", "").strip()

    def get_narrative_prompt(self, text):
        return '''Given a transcript, get narrative:
        
        Transcript: {text}
        
        Headline:'''.format(text=text)
