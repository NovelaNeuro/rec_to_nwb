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
            :var path: path where file should be saved
            :var url: url to file
    """

    url = ""
    path = ""

    def __init__(self,
                 url="https://www.dropbox.com/s/a7ddruxoffgbe7y/AC13_d27_WhereAreWeNow.rec?dl=1",
                 path="../data/file.rec"):
        self.url = url
        self.path = path

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
            if not os.path.isfile(self.path):
                self.start_downloading(self.url)

    def start_downloading(self, url):
        """ Start downloading from url and save file to default path

            Parameters:
                :param url: url to file
        """
        logging.info('Downloading package from: ', url)
        headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
        request = requests.get(url, stream=True, headers=headers)
        with open(self.path, 'wb') as binary_file:
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    binary_file.write(chunk)
