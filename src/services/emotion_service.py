from transformers import pipeline
from flask_restful import current_app as app
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

class emotion_service:

    def __init__(self):
        self.device, self.classifier, self.tokenizer, self.model = self.initialize_model()

    def initialize_model(self):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        classifier = pipeline("text-classification", 
                              model="j-hartmann/emotion-english-distilroberta-base", 
                              top_k=1,
                              device=device)
        tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")  
        model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base").to(device)

        # Label mappings
        self.emotion_mapping = {
            'LABEL_0': 'anger',
            'LABEL_1': 'disgust',
            'LABEL_2': 'fear',
            'LABEL_3': 'joy',
            'LABEL_4': 'neutral',
            'LABEL_5': 'sadness',
            'LABEL_6': 'surprise'
        }

        return device, classifier, tokenizer, model

    def get_emotions(self, texts):
        app.logger.info('Entering get_emotions')
    
        # Perform emotion classification
        with torch.no_grad():
            outputs = self.classifier(texts)  # Pass a list of texts directly to the classifier
            app.logger.info(texts)
            app.logger.info(outputs)
        # Extract the predicted emotions and scores (note the double indexing [0][0])
            predicted_emotions = [output[0]['label'] for output in outputs]
            predicted_scores = [output[0]['score'] for output in outputs]
            app.logger.info(predicted_emotions)

            # Create a list of dictionaries containing both emotion and score
            emotions = [{'emotion': emotion, 'score': score} for emotion, score in zip(predicted_emotions, predicted_scores)]
            app.logger.info(emotions)

        return emotions