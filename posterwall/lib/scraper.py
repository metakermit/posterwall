from urllib.parse import urljoin
import urllib
import io
import gzip
import webbrowser
import logging
import sys

import requests
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from bs4 import BeautifulSoup
from PIL import ImageFile

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

#TODO: check gzip
def _fetch_url(url, referer=None, session=None):
    response = session.get(url).result()
    return response.headers['content-type'], response.text

#TODO: cache (for multiple links to the same image) !!!
# (the image download is now ~ to Chrome speed)
# http://requests-cache.readthedocs.org/en/latest/user_guide.html#usage

def _parallel_get_sizes(img_urls, session):
    future_to_url = {session.get(url, stream=True): url for url in img_urls}
    sizes = {}
    for future in as_completed(future_to_url):
        img_url = future_to_url[future]
        try:
            response = future.result()
            parser = ImageFile.Parser()
            for chunk in response.iter_content(chunk_size=32):
                if not chunk:
                    break
                parser.feed(chunk)
                if parser.image:
                    sizes[img_url] = parser.image.size
                    break
        except requests.RequestsException:
            sizes[img_url] = None
        finally:
            if response:
                response.close()
    return sizes

class Scraper(object):
    def __init__(self, url):
        self.url = url
        self.session = FuturesSession(max_workers=100)
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def _extract_image_urls(self, soup):
        for img in soup.findAll("img", src=True):
            yield urljoin(self.url, img["src"])

    def _find_thumbnail_image(self):
        content_type, content = _fetch_url(self.url, session=self.session)
        soup = BeautifulSoup(content)
        image_urls = self._extract_image_urls(soup)
        image_urls = [u for u in image_urls] # turn to list
        image_urls = list(set(image_urls)) # lose duplicates
        image_sizes = _parallel_get_sizes(image_urls, self.session)
        logging.debug('got sizes for {} images'.format(len(image_sizes)))
        # find biggest
        # TODO: use Reddit's procedure !!!
        max_area = 0
        max_url = None
        for image_url in image_urls:
            size = image_sizes[image_url]
            if not size:
                continue

            # ignore little images
            area = size[0] * size[1]
            if area < 5000:
                logging.debug('ignore little {}'.format(image_url))
                continue

            # ignore excessively long/wide images
            if max(size) / min(size) > 1.5:
                logging.debug('ignore dimensions {}'.format(image_url))
                continue

            # penalize images with "sprite" in their name
            if 'sprite' in image_url.lower():
                logging.debug('penalizing sprite {}'.format(image_url))
                area /= 10

            if area > max_area:
                max_area = area
                max_url = image_url
        return max_url


    def scrape(self):
        thumbnail_url = self._find_thumbnail_image()
        #thumbnail = _make_thumbnail_from_url(thumbnail_url, referer=self.url)
        return thumbnail_url

#link = "https://www.kset.org/dogadaj/2014-02-14-plesnjak-kino-valentinovo/"
link = "https://www.kset.org/dogadaj/2014-03-07-hladno-pivo/"
#link = "http://www.mochvara.hr/program/info/lynx-lynx-music-predstavlja-140419"

def test_scraper():
    scraper = Scraper(link)
    thumbnail = scraper.scrape()
    print('SCRAPER RESULT:')
    print(thumbnail)

if __name__=="__main__":
    test_scraper()
