import os

from flask_restful import current_app as app
from pytube import YouTube


class video_service:

    def get_audio_from_yt_video(self, video_id):
        url = 'https://www.youtube.com/watch?v=' + video_id
        youtube = YouTube(url)
        video = youtube.streams.filter(only_audio=True).first()
        output_directory = "temp_audios"
        os.path.join(output_directory, video_id + '.mp3')
        output_file = video.download(output_path=output_directory, filename=video_id)
        base, _ = os.path.splitext(output_file)
        new_output_file = base + '.mp3'
        os.rename(output_file, new_output_file)
        return new_output_file

    def download_videos(self, video_ids: list, destination: str = './data/videos'):
        video_ids = [*set(video_ids)]
        for video_id in video_ids:
            app.logger.info('Downloading video: ', video_id)
            self.download_video(video_id, destination)

    def download_video(self, video_id: str, destination: str = './data/videos'):
        try:
            video_url = 'https://www.youtube.com/watch?v=' + video_id
            YouTube(video_url).streams.filter(res='144p').first().download(output_path=destination,
                                                                           filename=video_id + '.3gpp')
            return destination + '/' + video_id + '.3gpp'
        except Exception as err:
            app.logger.error('Exception raised while downloading yt video: ', err)
