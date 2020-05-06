""" Module to download a file from url

Class:
    FileDownloader()
"""
import logging.config
import os

import requests

from fl.processing.tools.abstract_file_downloader import AbstractFileDownloader

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class FileDownloader(AbstractFileDownloader):
    """ Class to download a file

        Methods:
            download_file()
            start_downloading()

        Variable:
            :var download_path: path where file should be saved
            :var url: url to file
    """

    def __init__(self,
                 url="https://www.dropbox.com/s/a7ddruxoffgbe7y/AC13_d27_WhereAreWeNow.rec?dl=1",
                 download_path="../data/file.rec"):
        self.url = url
        self.download_path = download_path

    def download_file(self, url=""):
        """ Check if User type custom url. If yes, start downloading,
        if no check if file already exist.
        If no, start downloading from default url.

            Parameters:
                :param url: custom url to file
        """
        if url != '':
            self.start_downloading(url)
        else:
            if not os.path.isfile(self.download_path):
                self.start_downloading(self.url)

    def start_downloading(self, url):
        """ Start downloading from url and save file to default path

            Parameters:
                :param url: url to file
        """
        logger.info('Downloading package from: %s', url)
        headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
        request = requests.get(url, stream=True, headers=headers)
        with open(self.download_path, 'wb') as binary_file:
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    binary_file.write(chunk)
