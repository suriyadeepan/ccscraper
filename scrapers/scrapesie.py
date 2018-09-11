from bs4 import BeautifulSoup
import requests
import json
import os
from random import randint


def link2soup(link, headers=None):
    """
    Fetch contents from a URL as text
    Cast it into Soup

    Args:
        link (str): URL
    """
    return BeautifulSoup(requests.get(link, headers=headers).content)

def download_with_delays(urls, filenames, delay_min=5, delay_max=15):
    for url, filename in zip(urls, filenames):
        print(':: [download_with_delays] Downloading from "{}" to "{}"'.format( 
            url, filename ))
        download_through_requests(url, filename, timeout= 10+delay_min)
        # random delay
        delay = randint(delay_min, delay_max)
        print(':: [ ] Inserting delay of {} seconds'.format(delay))

def download_through_requests(url, filename, timeout=10):
    """
    Use requests module to download file, chunk by chunk

    Args:
        url      (str): url to download file
        filename (str): name to save file
        timeout  (int): [10] #seconds to wait to throw TimedOut exception
    """
    # fetch path to filename
    directory = '/'.join(filename.split('/')[:-1])
    # create directory if it doesn't exist
    mkdir(directory)

    try:
        request = requests.get(url, timeout=timeout, stream=True)
        with open(filename, 'wb') as f:
            for chunk in request.iter_content(1024*1024):
                f.write(chunk)
    except requests.exceptions.Timeout:
        print('Request timed out for "{}" !!'.format(url))

def mkdir(directory):
    """
    Make directory if it doesn't exist

    """
    if not os.path.exists(directory):
        os.makedirs(directory)
