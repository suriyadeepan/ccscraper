import scrapesie as F
import argparse
import os

from tqdm import tqdm

BASE = 'http://www.projectmadurai.org'
SEED = 'http://www.projectmadurai.org/pmworks.html'

parser = argparse.ArgumentParser()
parser.add_argument("--out", default='cc/', 
        help='[cc/] Folder to store downloaded content')
args = parser.parse_args()


def fetch_PDF_links():
    soup = F.link2soup(SEED)
    return [ BASE + a.attrs['href'] for a in soup.find_all('a')
            if 'href' in a.attrs and a.attrs['href'][-3:] == 'pdf' ]


if __name__ == '__main__':
    links = fetch_PDF_links()
    for link in tqdm(links):
        F.download_through_requests(
                url= link, 
                filename= os.path.join(args.out, link.split('/')[-1]), 
                timeout= 15)
