import os

import cv2
import numpy as np
from imutils.video import FileVideoStream, FPS
from flask_restful import current_app as app

from services.youtube.video_service import video_service

from services.sftp_service import sftp_service


class barcode_service:
    def __init__(self,
                 verbose: bool = True,
                 video_path: str = None,
                 barcode_width: int = 1):
        self.video_service = video_service()

        # Use the updated sftp_service with Paramiko
        self.sftp_service = sftp_service(
            host=os.environ.get('BARCODE_FTP_HOST'),
            username=os.environ.get('BARCODE_FTP_USERNAME'),
            password=os.environ.get('BARCODE_FTP_PASSWORD')
        )

        self.video_path = video_path
        self.video = None
        self.frame_averages = []
        self.verbose = verbose
        self.barcode = None
        self.barcode_height = 224
        self.barcode_width = barcode_width
        self.generate_features = True
        self.frame_count = 0
        self.video_fps = 0
        self.video_width = None
        self.video_height = None
        self.elapsed_time = 0.0
        self.processed_frame_count = 0
        self.processed_video_width = 0
        self.processed_video_height = 0
        self.fps = 0
        self.fvs = None

    def generate_barcodes(self, json_request):
        video_ids = json_request['video_ids']
        self.generate_and_upload_barcodes(video_ids)
        response = {'message': "successful" }
        return response

    def generate_and_upload_barcodes(self, video_ids: list[str]):
        for video_id in video_ids:
            barcode_file = self.generate_barcode(video_id)

           

    def generate_barcode(self, video_id: str) -> str:
        self.video_path = self.video_service.download_video(video_id)
        print('\nvideo_path: ', self.video_path)
        return self.convert_video_to_barcode(self.video_path, video_id=video_id)

    def convert_video_to_barcode(self,
                                 video_file: str,
                                 destination: str = './data/barcodes',
                                 colors: list = None,
                                 video_id: str = None):
        self.video_path = video_file
        if not os.path.exists(destination):
            os.makedirs(destination)
        if colors is None:
            self.get_frames_averages()
        else:
            self.frame_averages = colors
        self.barcode = np.zeros((self.barcode_height, len(self.frame_averages), 3), dtype="uint8")
        for (i, avg) in enumerate(np.array(self.frame_averages)):
            cv2.rectangle(self.barcode,
                          (int(i * self.barcode_width), 0),
                          (int((i + 1) * self.barcode_width), self.barcode_height),
                          (int(avg[0]), int(avg[1]), int(avg[2])), 3)
        if self.verbose:
            app.logger.info("Barcode is being calculated ...")

        barcode_file_path = os.path.join(destination, f'{video_id}.png')

        print('\nbarcode_file_path: ', barcode_file_path)

        cv2.imwrite(filename=barcode_file_path, img=self.barcode)
        # Explicitly release resources 
        cv2.destroyAllWindows()

        # upload logic here, after the file is written to disk
        if os.path.exists(barcode_file_path):
            print('File exists. Uploading...')
            self.upload_barcode(barcode_file_path, video_id)
        else:
            app.logger.error('File not found after writing: %s', barcode_file_path)

        return barcode_file_path

        

    def get_frames_averages(self):
        """
        Calculate frames' average pixel values for all frames of loaded video
        :return: build the list for average pixel values
        """
        if self.video is None:
            self.load_video()

        # Start video stream
        if self.verbose:
            app.logger.debug(f"Video is being started ..")
        self.fvs = self.video.start()
        fps = FPS().start()

        # Generate video features before processing
        if self.generate_features:
            self.frame_count = int(self.video.stream.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_fps = int(self.video.stream.get(cv2.CAP_PROP_FPS))
            self.video_width = int(self.video.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(self.video.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

            if self.verbose:
                app.logger.info(f"[Video] frame count: {self.frame_count}")
                app.logger.info(f"[Video] FPS: {self.video_fps}")
                app.logger.info(f"[Video] Size: {self.video_width} x {self.video_height}")

        # Loop frames in a while
        if self.verbose:
            app.logger.info(f"Video frame average pixel values are being calculated ..")
        while self.fvs.more():
            frame = self.fvs.read()
            self.frame_averages.append(cv2.mean(frame)[:3])
            fps.update()
        fps.stop()
        self.fvs.stop()

        # Generate video features after processing
        if self.generate_features:
            self.fps = int(fps.fps())
            self.elapsed_time = fps.elapsed()
            self.processed_frame_count = fps.elapsed() * fps.fps()
            self.processed_video_width = int(self.video_width)
            self.processed_video_height = int(self.video_height)
            if self.verbose:
                app.logger.info(f"[Processed] frame count: {self.frame_count}")
                app.logger.info(f"[Processed] FPS: {self.fps}")
                app.logger.info(f"[Processed] Size: {self.processed_video_width} x {self.processed_video_height}")

    def load_video(self):
        """
        Accelerated video stream with multi-threading support
        :return:
        """
        if self.verbose:
            app.logger.info(f"{self.video_path} is loading ..")
        if self.if_exist():
            self.video = FileVideoStream(self.video_path)

    def if_exist(self):
        """
        For provided video path, check if it exists
        :return: The result of if the video exists
        """
        if not os.path.exists(self.video_path):
            app.logger.info(f"{self.video_path} doesn't exist!")
            return False
        return True

    def upload_barcode(self, barcode_file, video_id):
        # Construct the absolute barcode file path
        barcode_file_path = os.path.abspath(os.path.join('data/barcodes', f'{video_id}.png'))

        # Print the file path for debugging
        print('barcode_file_path:', barcode_file_path)

        # Print the contents of the directory for debugging
        print('Directory contents:', os.listdir('data/barcodes'))

        # Ensure the file exists before attempting to upload
        if os.path.exists(barcode_file_path):
            print('File exists. Uploading...')
            self.sftp_service.upload_file(
                local_file_path=barcode_file_path,
                sftp_folder_path='/home/cosmosadmin/Youtube/barcodes',
                remote_file_name=f'{video_id}.png'
            )
            self.sftp_service.close_connection()
        else:
            app.logger.error('File not found: %s', barcode_file_path)
