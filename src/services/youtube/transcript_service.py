from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed

from flask_restful import current_app as app

from services.youtube.translate_service import translate_service
from services.youtube.speech_to_text_service import speech_to_text_service


class transcript_service:

    def __init__(self):
        self.speech_to_text_service = speech_to_text_service()
        self.translate_service = translate_service()

    def get_video_transcripts(self, transcript_request):
        video_ids = transcript_request['video_ids']
        transcripts_from_ytapi = self.get_transcripts_from_ytapi(video_ids)
        full_transcripts = self.get_transcripts_from_whisper(transcripts_from_ytapi)
        translated_transcripts = self.translate_transcripts(full_transcripts)
        return translated_transcripts

    def get_transcripts_from_ytapi(self, video_ids):
        app.logger.info('Triggered youtube-transcript-api on %d video_ids', len(video_ids))
        transcripts = []
        for video_id in video_ids:
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                video_transcript = transcript_list[0].translate('en').fetch()[0]['text']
            except YouTubeRequestFailed as yt_error:
                app.logger.error('YouTubeRequestFailed on video_id: %s, error: %s', video_id, yt_error.ERROR_MESSAGE)
                video_transcript = 'No transcription'
            except Exception as error:
                app.logger.error('Video transcription error: %s on video_id: %s', error, video_id)
                video_transcript = 'No transcription'
            transcripts.append({
                'video_id': video_id,
                'transcript': video_transcript
            })
        return transcripts

    def get_transcripts_from_whisper(self, transcripts):
        for i in range(len(transcripts)):
            if transcripts[i]['transcript'] == 'No transcription':
                video_id = transcripts[i]['video_id']
                app.logger.info('Triggering whisper model for video_id: %s', video_id)
                whisper_transcript = self.speech_to_text_service.get_video_transcript(video_id)
                transcripts[i]['transcript'] = whisper_transcript
        return transcripts

    def translate_transcripts(self, transcripts):
        app.logger.info('Triggering translate on %d video_ids', len(transcripts))
        return \
            self.translate_service \
                .refine_and_translate_transcripts(transcripts)
