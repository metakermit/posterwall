import requests
from bs4 import BeautifulSoup

link = "https://www.kset.org/dogadaj/2014-02-14-plesnjak-kino-valentinovo/"

resp = requests.get(link)
html = resp.text
soup = BeautifulSoup(html)
images = soup.find_all('img')
print(images)

#TODO: check size and choose based on that

import webbrowser

img = images[0]
img_url = img.attrs['src']
print('opening: ' + img_url)
webbrowser.open(img_url)
