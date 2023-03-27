import asyncio
import os.path
import time
import requests
from bs4 import BeautifulSoup as bS
from src.image_downloader import download_images_async

# request the wall street journal  website
WEBSITE_LINK = 'https://www.bbc.com/news/science-environment-56837908'
WEBSITE = bS(requests.get(WEBSITE_LINK).content, "html.parser")
IMAGE_DIRECTORY = "BBC\\"
LOGO = os.path.join("Assets", "BBC-Logo.png")
# this storage will hold the articles of wall st in format :
# [['headline_text', 'image_path', 'article_link', 'article_author', 'publish_date', 'excerpt']

article_details = []
image_links = []  # stores the links for the images
articles = bS.findParent(bS.find(WEBSITE, 'h2', attrs={'id': 'latest-updates'})).find('div').find('div').find('ol').find_all('li', attrs={'class': 'lx-stream__post-container'}, limit=5)


async def scrape():
    if not os.path.exists(IMAGE_DIRECTORY):
        os.mkdir(IMAGE_DIRECTORY)

    number = 0
    for article in articles:

        try:
            article_link = "https://www.bbc.com" + article.find('a', attrs={'class': 'qa-heading-link lx-stream-post__header-link'})['href']
        except TypeError:
            continue
        except AttributeError:
            continue

        headline_text = article.find('span', attrs={'class': 'lx-stream-post__header-text gs-u-align-middle'}).text

        try:
            image_link = article.find('img', attrs={'class': 'qa-srcset-image lx-stream-related-story--index-image qa-story-image'})['src']
        except TypeError:
            image_link = 'none'
        except AttributeError:
            image_link = 'none'

        try:
            publish_date = article.find('time').find('span', attrs={'class': 'qa-post-auto-meta'}).text
        except AttributeError:
            publish_date = 'none'
        try:
            article_author = article.find('p', attrs={'class': 'qa-contributor-name'}).text
        except AttributeError:
            article_author = 'none'

        try:
            excerpt = article.find('p', attrs={'class': 'qa-story-summary'}).text
        except AttributeError:
            excerpt = 'none'

        image_links.append(image_link)

        article_details.append([headline_text, (f'{IMAGE_DIRECTORY}\\{number}BBC.jpg' if image_link != 'none' else 'none'),
                                (article_link if article_link != 'none' else 'none'), article_author, publish_date, excerpt, LOGO])

        number += 1

    await download_images_async(image_links, IMAGE_DIRECTORY, 'BBC.jpg')

    return article_details

