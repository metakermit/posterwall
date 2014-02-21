from urllib.parse import urljoin
import urllib
import io
import gzip
import webbrowser

import requests
from bs4 import BeautifulSoup
from PIL import ImageFile

#TODO: check gzip
def _initialize_request_old(url, referer):

    if not url.startswith(("http://", "https://")):
        return

    req = urllib.request.Request(url)
    req.add_header('Accept-Encoding', 'gzip')
    #if g.useragent:
    #    req.add_header('User-Agent', g.useragent)
    if referer:
        req.add_header('Referer', referer)
    return req

def _initialize_request(url, referer):
    pass

def _fetch_url_old(url, referer=None):
    request = _initialize_request(url, referer=referer)
    if not request:
        return None, None
    response = urllib.request.urlopen(request)
    response_data = response.read()
    content_encoding = response.info().get("Content-Encoding")
    if content_encoding and content_encoding.lower() in ["gzip", "x-gzip"]:
        buf = io.BytesIO(response_data)
        f = gzip.GzipFile(fileobj=buf)
        response_data = f.read()
    return response.headers.get("Content-Type"), response_data

def _fetch_url(url, referer=None, session=None):
    if session:
        response = session.get(url)
    else:
        response = requests.get(url)
    return response.headers['content-type'], response.text


#TODO: cache (for multiple links to the same image) !!!
# http://requests-cache.readthedocs.org/en/latest/user_guide.html#usage
def _fetch_image_size_old(url, referer):
    """Return the size of an image by URL downloading as little as possible."""

    request = _initialize_request_old(url, referer)
    if not request:
        return None

    parser = ImageFile.Parser()
    response = None
    try:
        response = urllib.request.urlopen(request)

        while True:
            chunk = response.read(1024)
            if not chunk:
                break

            parser.feed(chunk)
            if parser.image:
                return parser.image.size
    except urllib.error.URLError:
        return None
    finally:
        if response:
            response.close()

def _fetch_image_size(url, referer, session=None):
    """Return the size of an image by URL downloading as little as possible."""

    parser = ImageFile.Parser()
    response = None
    try:
        if session:
            response = session.get(url, stream=True)
        else:
            response = requests.get(url, stream=True)
        while True: # TODO: inspect this - new SSL handshakes every time
            chunk = response.raw.read(1024)
            if not chunk:
                break
            parser.feed(chunk)
            if parser.image:
                return parser.image.size
    except requests.RequestException:
        return None
    finally:
        if response:
            response.close()

#TODO: profile, something is too slow
# -> ssl handshake on every request
class Scraper(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def _extract_image_urls(self, soup):
        for img in soup.findAll("img", src=True):
            yield urljoin(self.url, img["src"])

    def _find_thumbnail_image(self):
        # _fetch_content
        content_type, content = _fetch_url(self.url, session=self.session)
        #resp = requests.get(self.url)
        #html = resp.text
        soup = BeautifulSoup(content)
        image_urls = self._extract_image_urls(soup)
        # find biggest
        # TODO: use Reddit's procedure
        max_size = (0, 0)
        max_url = None
        for image_url in image_urls:
            size = _fetch_image_size(image_url, referer=self.url,
                                     session=self.session)
            if not size:
                continue
            if size > max_size:
                max_size = size
                max_url = image_url
        return max_url


    def scrape(self):
        thumbnail_url = self._find_thumbnail_image()
        #thumbnail = _make_thumbnail_from_url(thumbnail_url, referer=self.url)
        return thumbnail_url

#link = "https://www.kset.org/dogadaj/2014-02-14-plesnjak-kino-valentinovo/"
link = "https://www.kset.org/dogadaj/2014-03-07-hladno-pivo/"

def get_image_urls_on_page(link):
    session = requests.Session()
    resp = session.get(link)
    html = resp.text
    soup = BeautifulSoup(html)
    images = soup.find_all('img')
    print(images)

    img = images[0]
    img_url = img.attrs['src']
    print('opening: ' + img_url)
    webbrowser.open(img_url)

def test_get_image_size():
    session = requests.Session()
    img_url = "https://www.kset.org/media/uploads/program/_2014/2014-02-14_valentinovo_fb_thumb.jpg"
    #import pdb; pdb.set_trace()
    size = _fetch_image_size(img_url, link, session=session)
    print(size)

#test_get_image_size()

def test_scraper():
    scraper = Scraper(link)
    thumbnail = scraper.scrape()
    print(thumbnail)

if __name__=="__main__":
    test_scraper()
