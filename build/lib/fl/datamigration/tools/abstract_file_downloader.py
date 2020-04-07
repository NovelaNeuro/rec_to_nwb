""" Module with Interface to download a file

Class:
    AbstractFileDownloader()
"""
from abc import abstractmethod


class AbstractFileDownloader:
    """ Interface to download a file

        Abstract methods:
            download_file()
            start_downloading()
    """

    @abstractmethod
    def download_file(self, url):
        """ Check parameters and call start_downloading(url)

            Parameters:
                :param url: custom url to file
        """

    @abstractmethod
    def start_downloading(self, url):
        """ Start downloading from url

            Parameters:
                :param url: url to file
        """
