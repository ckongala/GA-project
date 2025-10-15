import os
import paramiko
from flask_restful import current_app as app

class sftp_service:

    def __init__(self, host, username, password):
        self.transport = paramiko.Transport((host, 22))
        try:
            self.transport.connect(username=username, password=password)
            app.logger.info('SFTP connection established successfully.')
        except Exception as e:
            app.logger.error('Error establishing SFTP connection: %s', e)
            raise
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

  
    def upload_file(self, local_file_path, sftp_folder_path, remote_file_name=None):
        app.logger.info('Preparing to upload file: %s', local_file_path)
        absolute_path = os.path.abspath(local_file_path)
        app.logger.info('Absolute path: %s', absolute_path)

        # Default to the same file name if remote_file_name is not provided
        if not remote_file_name:
            remote_file_name = os.path.basename(absolute_path)

        try:
            # Check if the folder exists, create if not
            try:
                self.sftp.listdir(sftp_folder_path)
            except IOError as e:
                app.logger.info('Folder not found, creating folder on SFTP server: %s', sftp_folder_path)
                self.sftp.mkdir(sftp_folder_path)

            # Set the remote working directory
            self.sftp.chdir(sftp_folder_path)

            # Confirm file existence before upload
            if os.path.exists(absolute_path):
                app.logger.info('Confirmed file exists at: %s', absolute_path)
                # Upload the file with the specified remote filename
                self.sftp.put(absolute_path, remote_file_name)
                app.logger.info('File uploaded successfully: %s', remote_file_name)
            else:
                app.logger.error('File does not exist at: %s', absolute_path)

        except FileNotFoundError as err:
            app.logger.error('Local file not found for upload: %s, %s', err, local_file_path)
        except Exception as e:
            app.logger.error('Error during file upload: %s', str(e))



    def download_file(self, sftp_file_path, local_folder_path):
        app.logger.info('Downloading %s to local folder: %s', sftp_file_path, local_folder_path)
        if not os.path.isdir(local_folder_path):
            os.makedirs(local_folder_path)
        try:
            self.sftp.get(sftp_file_path, os.path.join(local_folder_path, os.path.basename(sftp_file_path)))
        except FileNotFoundError:
            app.logger.error('File %s does not exist on SFTP server', sftp_file_path)
            
    def list_directory_contents(self, sftp_folder_path):
        try:
            contents = self.sftp.listdir(sftp_folder_path)
            app.logger.info('Contents of %s: %s', sftp_folder_path, contents)
            return contents
        except Exception as e:
            app.logger.error('Error listing directory contents: %s, %s', sftp_folder_path, str(e))

    def delete_file(self, sftp_file_path):
        app.logger.info('Deleting %s from SFTP server', sftp_file_path)
        try:
            self.sftp.remove(sftp_file_path)
        except FileNotFoundError:
            app.logger.error('File %s does not exist on SFTP server', sftp_file_path)

    def close_connection(self):
        app.logger.info('Closing SFTP connection...')
        self.sftp.close()
        self.transport.close()
