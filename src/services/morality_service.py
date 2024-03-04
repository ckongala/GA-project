from flask_restful import current_app as app

import pandas as pd 

from emfdscore.scoring import score_docs



class morality_service():

    def __init__(self):
        self.DICT_TYPE = 'emfd'
        self.PROB_MAP = 'all'
        self.SCORE_METHOD = 'bow'
        self.OUT_METRICS = 'vice-virtue'
        


    def calculate_morality(self, data:list):
        """
        Calculating the morality for the given Text.
        
        """
        response = []
        num_items = len(data)
        title_text_data = []
        urls = []
        for i in range(num_items):
            title_text_data.append(data[i]["text"])
            urls.append(data[i]["url"])
            pass 
        df = pd.DataFrame(title_text_data)
        df.columns=[0]
        edf = score_docs(df, self.DICT_TYPE, self.PROB_MAP, self.SCORE_METHOD, self.OUT_METRICS, num_items)
        for k in range(num_items):
            output = {
                "url" : urls[k],
                "morality": {"Care": edf["care.virtue"][k],
                            "Fairness": edf["fairness.virtue"][k],
                            "Loyality": edf["loyalty.virtue"][k],
                            "Authority": edf["authority.virtue"][k],
                            "Sanctity": edf["sanctity.virtue"][k],
                            "Harm": edf["care.vice"][k],
                            "Cheating": edf["fairness.vice"][k],
                            "Betrayal": edf["loyalty.vice"][k],
                            "Subversion": edf["authority.vice"][k],
                            "Degradation": edf["sanctity.vice"][k],
                            "moral_nonmoral_ratio": edf["moral_nonmoral_ratio"][k],
                            "f_var" : edf["f_var"][k]}
            }
            response.append(output)
        return response
        
        




