from os import environ

import openai
from openai import ErrorObject as openai_error

from flask_restful import current_app as app


class gpt3_keywords_service:

    def __init__(self):
        openai.api_key = environ.get('OPENAI_API_KEY')
        self.engine = "davinci-instruct-beta-v3"
        self.temperature = 0
        self.max_tokens = 10
        self.top_p = 1
        self.frequency_penalty = 0
        self.presence_penalty = 0

    def get_keywords(self, request_json):
        chunks = request_json['chunks']
        app.logger.info('Requesting GPT3 for keywords in %d transcripts', len(chunks))
        keywords_list = []
        for chunk in chunks:
            keywords_list.append(self.get_keywords_from_text(chunk))
        return {
            'keywords_list': keywords_list
        }

    def get_keywords_from_text(self, text: str):
        keywords = None
        try:
            openai_response = openai.Completion.create(
                engine=self.engine,
                prompt=self.get_keywords_prompt(text),
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )
            keywords = openai_response.choices[0].text
            keywords = keywords[:-1] if keywords.endswith(",") else keywords
        except openai_error:
            app.logger.info('OpenAI Exception occurred, Exception: ', openai_error)
        except Exception as error:
            app.logger.info('Exception occurred while getting keywords from gpt3, Exception: ', error)
        return keywords.replace("\n", "").strip()

    def get_keywords_prompt(self, text):
        return '''Given a transcript, get tags:
        
        Transcript: {text}
        
        Tags:'''.format(text=text)
