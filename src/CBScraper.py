import asyncio
import os.path
import time
import requests
from bs4 import BeautifulSoup as bS
from image_downloader import download_images_async
from tqdm import tqdm

# request the wall street journal  website
WEBSITE_LINK = 'https://www.cbsnews.com/search/?q=climate'

response = requests.get(WEBSITE_LINK)
time.sleep(10)

WEBSITE = bS(response.content, "html.parser")
IMAGE_DIRECTORY = "CBS\\"

target_number_of_articles = 10  # number of max articles to find

# this storage will hold the articles of wall st in format :
# [['headline_text', 'image_path', 'article_link', 'author_name', 'publish_date', 'excerpt']
article_details = []
image_links = []  # stores the links for the images
articles = [x.find('article') for x in bS.find_all(WEBSITE, 'div', attrs={'class': 'component__item-wrapper'}, limit=target_number_of_articles)]

def scrape():
    if not os.path.exists(IMAGE_DIRECTORY):
        os.mkdir(IMAGE_DIRECTORY)

    number = 0
    for article in articles:

        article_link = article.find('a')['href']

        headline_text = article.find('h4', attrs={'class': 'item__hed'}).text

        try:
            image_link = article.find('img')['src']
        except TypeError:
            image_link = 'none'

        try:
            publish_date = article.find('span', attrs={'class': 'item__date'}).text
        except AttributeError:
            publish_date = 'none'

        try:
            excerpt = article.find('p', attrs={'class': 'qa-story-summary'}).text
        except AttributeError:
            excerpt = 'none'

        image_links.append(image_link)

        article_details.append([headline_text, (f'{number}CBS.jpg' if image_link != 'none' else 'none'),
                                (article_link if article_link != 'none' else 'none'), "none", publish_date, excerpt])

        image_links.append(image_link)

        number += 1

    asyncio.run(download_images_async(image_links, IMAGE_DIRECTORY, 'CBS.jpg'))

    return article_details
