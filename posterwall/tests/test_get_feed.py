from nose.tools import *

from posterwall.lib import get_feed

def test_get_image_url():
    # TODO: stub that works with html files
    n = 3
    news = get_feed.read_news('http://kermit.epska.org/', n)
    assert_equal(len(news), n)

