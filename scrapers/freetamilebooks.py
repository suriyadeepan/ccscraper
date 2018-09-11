from bs4 import BeautifulSoup
import requests
import argparse
import os

from pprint import pprint as pp
from tqdm import tqdm

import scrapesie as F

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

BASE_URL = 'http://freetamilebooks.com'
PAGES_MAX = 28
PAGE_URL_FORMAT = '/'.join([ BASE_URL, 'page', '{}', ''])

parser = argparse.ArgumentParser()
parser.add_argument("--urls", default='cc/freetamilepubs.list', 
        help='[cc/] Folder to store downloaded content')
parser.add_argument("--out", default='cc/freetamilebooks/', 
        help='[cc/] Folder to store downloaded content')
args = parser.parse_args()


def fetch_links_containing(url, key):
    return [ link.get('href')
            for link in F.link2soup(url, headers=HEADERS).find_all('a') 
            if 'href' in link.attrs and key in link.text ]

def generate_pages():
    return [ PAGE_URL_FORMAT.format(i) 
            for i in range(1, PAGES_MAX+1) ]

def fetch_books(url):
    links = []
    for link in F.link2soup(url, headers=HEADERS).find_all('a'):
        if 'href' in link.attrs:
            if '/ebooks/' in link.get('href'):
                links.append(link.get('href'))
    return list(set(links))


if __name__ == '__main__':
    books = [ fetch_books(url) for url in tqdm(generate_pages()) ]
    books = [ i for l in books for i in l ]
    epubs = [ fetch_links_containing(book, 'epub') 
            for book in tqdm(books) ]
    for i,b in enumerate(epubs):
        print(i+1, b)
    with open(args.urls, 'r') as f:
        lines = [ l.replace('\n', '') for l in f.readlines() ]
    
    F.download_with_delays(lines,
            filenames= [ os.path.join(args.out, str(i)) + '.pdf' 
                for i in range(len(lines)) ]
            )
