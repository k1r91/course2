import urllib.request
import os
from bs4 import BeautifulSoup
import threading
from time_it import time_it


"""
Download MAX_COUNT images of specified theme from https://pexels.com
"""

MAX_COUNT = 5
DOWNLOAD_DIR = 'download'


def get_content(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(url, None, headers)
    result = urllib.request.urlopen(request)
    return result.read()


def download_image(url, path_to):
    opener = urllib.request.build_opener()
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    opener.addheaders = [('User-Agent', user_agent)]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, path_to)

@time_it
def main():
    theme = 'cars'
    link = 'https://pexels.com/search/{}/'.format(theme)
    content = get_content(link)
    soup = BeautifulSoup(content, 'html.parser')
    for item in soup.find_all('a', {'class': 'js-photo-link'}, formatter=None)[:MAX_COUNT]:
        link = ''.join(['https://www.pexels.com', item['href'].replace('&amp;', '&')])
        img_page = get_content(link)
        soup_img = BeautifulSoup(img_page, 'html.parser')
        for item in soup_img.find_all('img', {'class': 'image-section__image js-photo-zoom'}):
            img_link = item['src'].split('?')[0]
            download_filename = os.path.join(DOWNLOAD_DIR, img_link.split('/')[-1])
            task = threading.Thread(target=download_image, args=(img_link, download_filename))
            task.start()

@time_it
def main_v2():
    theme = 'nature'
    link = 'https://pexels.com/search/{}/'.format(theme)
    content = get_content(link)
    soup = BeautifulSoup(content, 'html.parser')
    for item in soup.find_all('a', {'class': 'js-photo-link'}, formatter=None)[:MAX_COUNT]:
        link = ''.join(['https://www.pexels.com', item['href'].replace('&amp;', '&')])
        img_page = get_content(link)
        soup_img = BeautifulSoup(img_page, 'html.parser')
        for item in soup_img.find_all('img', {'class': 'image-section__image js-photo-zoom'}):
            img_link = item['src'].split('?')[0]
            download_filename = os.path.join(DOWNLOAD_DIR, img_link.split('/')[-1])
            download_image(img_link, download_filename)


if __name__ == '__main__':
    main()