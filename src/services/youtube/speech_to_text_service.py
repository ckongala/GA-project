import os

from flask_restful import current_app as app
from whisper import load_model

from services.youtube.video_service import video_service

class speech_to_text_service:

    def __init__(self):
        self.whisper_model = load_model('base')
        self.video_service = video_service()

        pass

    def get_video_transcript(self, video_id):
        transcript = ''
        try:
            audio_file = self.video_service.get_audio_from_yt_video(video_id)
            whisper_result = self.whisper_model.transcribe(audio_file, fp16=False)
            transcript = whisper_result['text']
            if os.path.exists(audio_file):
                os.remove(audio_file)
            else:
                app.logger.warn('File does not exist: %s', audio_file)
            return transcript
        except Exception as error:
            app.logger.info(
                'Exception occurred while running whisper model on video_id: %s, error: %s',
                video_id,
                error)
        return transcript

