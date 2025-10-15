import math
import re

from flask_restful import current_app as app
from nltk import tokenize, download
from nltk.corpus import stopwords

from services.named_entity_service import named_entity_service
from utils.youtube.tfidf_utils import tfidf_utils


class tfidf_narrative_service:

    def __init__(self):
        self.named_entity_service = named_entity_service()
        self.tfidf_utils = tfidf_utils()

    def generate_tfidf_narratives(self, json_request):
        raw_text = json_request['raw_text']
        tfidf_narratives, entities = [], []
        app.logger.info('Generating tfidf narratives for %d raw texts', len(raw_text))
        for txt in raw_text:
            generated_narratives = self.generate_tfidf_narrative(txt)
            tfidf_narratives.append(generated_narratives[0])
            entities.append(generated_narratives[1])
        return {
            'tfidf_narratives': tfidf_narratives,
            'entities': entities
        }

    def generate_tfidf_narrative(self, txt: str):
        char_chunk_size = 7800
        number_of_chunks = math.ceil(len(txt) / char_chunk_size)
        tfidf_narratives, keywords = set(), set()
        for index in range(number_of_chunks):
            if index == number_of_chunks - 1:
                current_txt = txt[index * char_chunk_size:]
            else:
                current_txt = txt[index * char_chunk_size: (index + 1) * char_chunk_size]
            stop_words = self.get_stopwords()
            clean_text = self.clean_raw_text(current_txt)
            tfidf_text = self.tfidf_utils.pos_tag_narratives(clean_text)
            narratives_text = self.tfidf_utils.run_comprehensive(tfidf_text, stop_words)
            basic_narratives = tokenize.sent_tokenize(narratives_text)
            chunk_keywords = self.named_entity_service.get_top_named_entities(clean_text)
            chunk_tfidf_narratives = self.get_entity_matching_narratives(keywords, basic_narratives)
            keywords.update(chunk_keywords)
            tfidf_narratives.update(chunk_tfidf_narratives)
        return list(tfidf_narratives), list(keywords)

    def get_stopwords(self):
        download('punkt')
        download('stopwords')
        download('averaged_perceptron_tagger')
        return list(set(stopwords.words('english')))

    def clean_raw_text(self, raw_text):
        unique_sentences = []
        clean_text = ''
        for sentence in tokenize.sent_tokenize(raw_text):
            sentence = sentence.replace("'s", "s")
            sentence = re.sub(r"[-()\"#/@;:<>{}`'’‘“”+=–—_…~|!?]", " ", sentence)
            if ('on Twitter' not in sentence
                    and 'or e-mail to:' not in sentence
                    and 'd.getElementsByTagName' not in sentence
                    and len(sentence) > 10 and 'g.__ATA.initAd' not in sentence
                    and 'document.body.clientWidth' not in sentence):
                if sentence not in unique_sentences:
                    unique_sentences.append(sentence)
                    clean_text += str(' ') + str(sentence)
        return clean_text

    def get_entity_matching_narratives(self, keywords, basic_narratives):
        narratives = set()
        for narrative in basic_narratives:
            for keyword in keywords:
                if keyword.lower() in narrative.lower() and len(keyword) > 1:
                    narratives.add(narrative)
        if len(narratives) > 0:
            return list(narratives)
        if len(basic_narratives) > 15:
            return basic_narratives[:15]
        return basic_narratives
