import requests
from bs4 import BeautifulSoup
import webbrowser
import urllib
from PIL import ImageFile

#TODO: check size and choose based on that

def _clean_url(url):
    """url quotes unicode data out of urls"""
    #url = url.encode('utf8')
    #url = ''.join(urllib.quote(c) if ord(c) >= 127 else c for c in url)
    return url

def _initialize_request(url, referer):
    url = _clean_url(url)

    if not url.startswith(("http://", "https://")):
        return

    req = urllib.request.Request(url)
    req.add_header('Accept-Encoding', 'gzip')
    #if g.useragent:
    #    req.add_header('User-Agent', g.useragent)
    if referer:
        req.add_header('Referer', referer)
    return req

#TODO: cache (for multiple links to the same image)
def _fetch_image_size(url, referer):
    """Return the size of an image by URL downloading as little as possible."""

    request = _initialize_request(url, referer)
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



link = "https://www.kset.org/dogadaj/2014-02-14-plesnjak-kino-valentinovo/"

def get_image_urls_on_page(link):
    resp = requests.get(link)
    html = resp.text
    soup = BeautifulSoup(html)
    images = soup.find_all('img')
    print(images)

    img = images[0]
    img_url = img.attrs['src']
    print('opening: ' + img_url)
    webbrowser.open(img_url)

def test_get_image_size():
    img_url = "https://www.kset.org/media/uploads/program/_2014/2014-02-14_valentinovo_fb_thumb.jpg"
    #import pdb; pdb.set_trace()
    size = _fetch_image_size(img_url, link)
    print(size)

test_get_image_size()
