import asyncio
import os.path
import time
import requests
from bs4 import BeautifulSoup as bS
from src.image_downloader import *

# request the wall street journal  website
WEBSITE_LINK = 'https://edition.cnn.com/specials/world/cnn-climate'
WEBSITE = bS(requests.get(WEBSITE_LINK).content, "html.parser")
IMAGE_DIRECTORY = "CNN\\"
LOGO = os.path.join("Assets", "CNN-Logo.png")

target_number_of_articles = 5  # number of max articles to find

# this storage will hold the articles of wall st in format :
# ['headline_text', 'image_path', 'article_link', 'article_author', 'publish_date', 'excerpt', 'logo']
article_links = []
article_details = [[] for _ in range(target_number_of_articles)]
image_links = ["none" for _ in range(target_number_of_articles)]  # stores the links for the images
articles = bS.find_all(WEBSITE, 'article', limit=target_number_of_articles)


async def scrape():
    if not os.path.exists(IMAGE_DIRECTORY):
        os.mkdir(IMAGE_DIRECTORY)

    for article in articles:
        article_link = "none"
        try:
            article_link = "https://edition.cnn.com" + article.find('h3', attrs={'class': 'cd__headline'}).find("a")["href"]
        except TypeError:
            continue
        except AttributeError:
            continue

        article_links.append(article_link)

    await scrape_articles()
    await download_images_async(image_links, IMAGE_DIRECTORY, 'CNN.jpg')

    return article_details


async def scrape_articles():
    async with aiohttp.ClientSession() as session:  # asynchronously requests the image links
        await fetch_all_async(session)


async def fetch_all_async(session):
    tasks = []
    number = 0
    for article_link in article_links:
        if article_link != 'none':
            task = asyncio.create_task(scrape_article(session, article_link, number))
            tasks.append(task)  # creates the tasks that will be executed if there is a waiting time

        number += 1

    await asyncio.gather(*tasks)


async def scrape_article(session, article_link, number):
    try:
        async with session.get(article_link) as r:
            if r.status != 200:  # flags if the link leads to nowhere
                r.raise_for_status()

            html = bS(await r.content.read(), "html.parser")

            headline_text = html.find('h1', attrs={'data-editable': 'headlineText'}).text.strip()

            try:
                image_link = html.find('picture', attrs={'class': 'image__picture'}).find('img')['src']
            except AttributeError:
                image_link = 'none'
            except TypeError:
                image_link = 'none'

            try:
                article_author = html.find('span', attrs={'class': 'byline__name'}).text.strip()
            except AttributeError:
                article_author = 'none'
            except TypeError:
                article_author = 'none'

            try:
                publish_date = html.find('div', attrs={'class': 'timestamp'}).text.strip()
            except AttributeError:
                publish_date = 'none'
            except TypeError:
                publish_date = 'none'

            image_links[number] = image_link

            article_details[number] = [headline_text, (f'{IMAGE_DIRECTORY}\\{number}CNN.jpg' if image_link != 'none' else 'none'),
                                    (article_link if article_link != 'none' else 'none'), article_author, publish_date,
                                    "none", LOGO]
    except Exception:
        pass
