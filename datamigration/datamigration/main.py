import pathlib
import sys
import requests
import logging


def download_file(url):
    headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
    r = requests.get(url, stream=True, headers=headers)
    with open("../data/file.rec", 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def main():
    if len(sys.argv) > 1:
        logging.info('Downloading file from passed url')
        download_file(str(sys.argv[1]))
    elif not pathlib.Path('../data/file.rec').exists():
        logging.info('Downloading default file.rec')
        download_file("https://www.dropbox.com/s/a7ddruxoffgbe7y/AC13_d27_WhereAreWeNow.rec?dl=1")


if __name__ == "__main__":
    main()
