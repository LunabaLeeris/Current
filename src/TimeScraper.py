import asyncio
import os.path
import time
import requests
from bs4 import BeautifulSoup as bS
from src.image_downloader import *
from tqdm import tqdm

# request the wall street journal  website
WEBSITE_LINK = 'https://time.com/section/climate/'
WEBSITE = bS(requests.get(WEBSITE_LINK).content, "html.parser")
IMAGE_DIRECTORY = "TIME\\"
LOGO = os.path.join("Assets", "TIME-Logo.png")

target_number_of_articles = 5  # number of max articles to find

# this storage will hold the articles of wall st in format :
# ['headline_text', 'image_path', 'article_link', 'article_author', 'publish_date', 'excerpt', 'logo']
article_details = []
image_links = []  # stores the links for the images
articles = bS.find(WEBSITE, 'section', attrs={'class': 'section-related'}).find_all('div', attrs={'class': 'taxonomy-tout'}, limit=target_number_of_articles)


async def scrape():
    if not os.path.exists(IMAGE_DIRECTORY):
        os.mkdir(IMAGE_DIRECTORY)

    number = 0
    for article in articles:

        try:
            article_link = "https://time.com" + article.find('a')['href']
        except TypeError:
            continue
        except AttributeError:
            continue

        headline_text = article.find('h2', attrs={'class': 'headline'}).text.strip()

        try:
            image_link = article.find('div', attrs={'class': 'image-container'}).find('img')['src']
        except AttributeError:
            image_link = 'none'
        except TypeError:
            image_link = 'none'

        try:
            excerpt = article.find('h3', attrs={'class': 'summary'}).text.strip()
        except AttributeError:
            excerpt = 'none'
        except TypeError:
            excerpt = 'none'

        try:
            article_author = article.find('span', attrs={'class': 'byline'}).find_all('span')[0].text.strip()
        except AttributeError:
            article_author = 'none'
        except TypeError:
            article_author = 'none'

        try:
            publish_date = article.find('span', attrs={'class': 'byline'}).find_all('span')[1].text.strip()
        except AttributeError:
            publish_date = 'none'
        except TypeError:
            publish_date = 'none'

        image_links.append(image_link)

        article_details.append([headline_text, (f'{IMAGE_DIRECTORY}\\{number}TIME.jpg' if image_link != 'none' else 'none'),
                                (article_link if article_link != 'none' else 'none'), article_author, publish_date,
                                excerpt, LOGO])

        number += 1

    await download_images_async(image_links, IMAGE_DIRECTORY, 'TIME.jpg')

    return article_details
