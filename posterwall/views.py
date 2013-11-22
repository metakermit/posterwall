from django.http import HttpResponse
from get_feed import *

def home(request):
    all_news = []
    with open('places.txt') as places:
        urls = [line.rstrip() for line in places if line!='']
        for url in urls:
            feed_url = feed_on_site(url)
            news = read_news(feed_url)
            all_news.extend(news)
    return HttpResponse('Posterwall: ' + ',\n'.join(all_news))
    
