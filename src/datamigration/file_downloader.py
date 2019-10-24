""" Module to download a file from url

Class:
    DownloaderFile()
"""
import logging
import os

import requests

from src.datamigration.abstract_file_downloader import AbstractFileDownloader


class DownloaderFile(AbstractFileDownloader):
    """ Class to download a file

        Methods:
            download_file()
            start_downloading()

        Variable:
            :var download_path: path where file should be saved
            :var download_url: url to file
    """

    download_path = ""
    download_url = ""

    def __init__(self,
                 url="https://www.dropbox.com/s/a7ddruxoffgbe7y/AC13_d27_WhereAreWeNow.rec?dl=1",
                 path="../data/file.rec"):
        self.download_url = url
        self.download_path = path

    def download_file(self, alternative_url=""):
        """ Check if User type custom url. If yes, start downloading,
        if no check if file already exist.
        If no, start downloading from default url.

            Parameters:
                :param alternative_url: custom url to file
        """
        if alternative_url != "":
            logging.info('Starts downloading from custom url')
            self.start_downloading(alternative_url)
        else:
            if not os.path.isfile(self.download_path):
                logging.info('Starts downloading from default url')
                self.start_downloading(self.download_url)
            logging.info('File exist in default downloading_path')

    def start_downloading(self, url):
        """ Start downloading from url and save file to default path

            Parameters:
                :param url: url to file
        """
        logging.info('Downloading starts')
        headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
        request = requests.get(url, stream=True, headers=headers)
        with open(self.download_path, 'wb') as binary_file:
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    binary_file.write(chunk)
