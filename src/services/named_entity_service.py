from flask_restful import current_app as app

from collections import Counter

import en_core_web_sm


class named_entity_service:

    def __init__(self):
        app.logger.info('Initialized named_entity_service class')
        self.nlp = en_core_web_sm.load()

    def get_top_named_entities(self, text: str, top_n: int = 5):
        transcript_article = self.nlp(text)
        items = [x.text for x in transcript_article.ents]
        top_entities = Counter(items).most_common(top_n)
        return [entity[0] for entity in top_entities]
