from detoxify import Detoxify
from tqdm import tqdm
from textblob import TextBlob
import torch
import math

from flask_restful import current_app as app


class toxicity_service:

    def __init__(self):
        self.model = Detoxify("unbiased",
                              device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))  # device='cude'

    def get_toxicity_scores(self, data: list, process_sentiment: bool = True):
        """
        Giving arguments as data list.
        Returning the Toxicity scores.
        """
        app.logger.info('toxicity service initiated with data-size: %d, sentiment: %s', len(data),
                        str(process_sentiment))
        text = [row['text'] for row in data]
        return self.get_scores(text, self.model, process_sentiment)

    def get_scores(self, text, model, process_sentiment: bool):
        """
        Calculating the toxicity scores.
        """
        with torch.no_grad():
            if type(text) == str:
                if process_sentiment:
                    r = model.predict(text)
                    r['sentiment'] = self.get_sentiment(text)
                else:
                    r = model.predict(text)
                return r
            elif type(text) == list:
                results = []
                chunk_size = 100
                for l in tqdm(self.chunk_lst(text, chunk_size), desc="Processing Scores",
                              total=math.ceil(len(text) / chunk_size)):
                    if process_sentiment:
                        un_formatted_results = model.predict(l)
                        rows = [dict(zip(un_formatted_results, t)) for t in zip(*un_formatted_results.values())]
                        for r, t in zip(rows, l):
                            r['sentiment'] = self.get_sentiment(t)
                            results.append(r)
                    else:
                        un_formatted_results = model.predict(l)
                        results += [dict(zip(un_formatted_results, t)) for t in zip(*un_formatted_results.values())]
            return results

    def get_sentiment(self, text):
        """
        Giving arguments as text.
        Returning sentimental score. 
        """
        if not text:
            return None
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        sentiment_score_rounded = round(sentiment_score, 6)
        return sentiment_score_rounded

    def chunk_lst(self, lst: list, items_per_chunk: int):
        """Breaks a list into chunks
        Args:
            lst ([list]): List to chunk
            items_per_chunk ([int]): Number of items per list
        Yields:
            [list]: a chunk of lst, with size 'items_per_chunk'
        """
        for i in range(0, len(lst), items_per_chunk):
            yield lst[i:i + items_per_chunk]
