from bs4 import BeautifulSoup
import requests
import json


def link2soup(link, features='lxml'):
    """
    Fetch contents from a URL as text
    Cast it into Soup

    Args:
        link (str): URL
    """
    return BeautifulSoup(requests.get(link).text, features=features)

def download_through_requests(url, filename, timeout=10):
    """
    Use requests module to download file, chunk by chunk

    Args:
        url      (str): url to download file
        filename (str): name to save file
        timeout  (int): [10] #seconds to wait to throw TimedOut exception
    """
    try:
        request = requests.get(url, timeout=timeout, stream=True)
        with open(filename, 'wb') as f:
            for chunk in request.iter_content(1024*1024):
                f.write(chunk)
    except requests.exceptions.Timeout:
        print('Request timed out for "{}" !!'.format(url))
