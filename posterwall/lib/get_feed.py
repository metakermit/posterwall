from pyquery import PyQuery as pq

def feed_on_site(url):
    """find a site's RSS feed"""
    d = pq(url=url)
    link_element = d('link[type="application/rss+xml"]')[0]
    link_element.make_links_absolute(url)
    return link_element.attrib['href']

import feedparser

def recent_posts(feed_url, n):
    """return recent items from an RSS feed"""
    feed = feedparser.parse(feed_url)
    news = [item for item in feed['items'][:n]]
    #return feed['items'][:10]
    return news

def images_in_post(post_url):
    #TODO: one image for post
    d = pq(post_url)
    imgs = d('img')
    return [img.attrib['src'] for img in imgs]

def read_news(url, n=3):
    """get the list of posts from a site"""
    feed_url = feed_on_site(url)
    posts = recent_posts(feed_url, n)
    return posts

def main():
    with open('places.txt') as places:
        urls = [line.rstrip() for line in places if line!='']
        for url in urls:
            news = read_news(url)
            #news[15]['link']
            print(news)


if __name__ == '__main__':
    main()
