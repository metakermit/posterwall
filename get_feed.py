from pyquery import PyQuery as pq

def feed_on_site(url):
    d = pq(url=url)
    link_element = d('link[type="application/rss+xml"]')[0]
    link_element.make_links_absolute(url)
    return link_element.attrib['href']

import feedparser

def read_news(feed_url):
    feed = feedparser.parse(feed_url)
    #news = [item['summary'] for item in feed['items'][:3]]
    return feed['items'][:10]


def main():
    with open('places.txt') as places:
        urls = [line.rstrip() for line in places if line!='']
        for url in urls:
            feed_url = feed_on_site(url)
            news = read_news(feed_url)
            print(news)

main()
