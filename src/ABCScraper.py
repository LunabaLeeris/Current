import asyncio
import os.path
import time
import aiohttp
import requests
from bs4 import BeautifulSoup as bS
from tqdm import tqdm
from src.image_downloader import download_images_async

# request the wall street journal  website
WEBSITE_LINK = 'https://abcnews.go.com/Alerts/Weather'
LOGO = os.path.join("Assets", "ABC-Logo.png")
WEBSITE = bS(requests.get(WEBSITE_LINK).content, "html.parser")
IMAGE_DIRECTORY = "ABC\\"

target_number_of_articles = 5  # number of max articles to find

# this storage will hold the articles of wall st in format :
# [['headline_text', 'image_path', 'article_link', 'article_author', 'publish_date', 'excerpt']

article_links = []
article_details = [[] for _ in range(target_number_of_articles)]
image_links = ["none" for _ in range(target_number_of_articles)]  # stores the links for the images
articles = bS.find_all(WEBSITE, 'section', attrs={'class': 'ContentRoll__Item'}, limit=target_number_of_articles)


async def scrape():
    if not os.path.exists(IMAGE_DIRECTORY):
        os.mkdir(IMAGE_DIRECTORY)

    for article in articles:
        article_link = article.find('div', attrs={'class', 'ContentRoll__Headline'}).find('a')['href']
        headline_text = article.find('div', attrs={'class', 'ContentRoll__Headline'}).find('a').text

        try:
            excerpt = article.find('div', attrs={'class': 'ContentRoll__Desc'}).text
        except AttributeError:
            excerpt = 'none'
        except TypeError:
            excerpt = 'none'

        article_links.append([article_link, headline_text, excerpt])

    await scrape_articles()
    await download_images_async(image_links, IMAGE_DIRECTORY, 'ABC.jpg')

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
        async with session.get(article_link[0]) as r:
            if r.status != 200:  # flags if the link leads to nowhere
                r.raise_for_status()

            html = bS(await r.content.read(), "html.parser")

            try:
                image_link = html.find('div', attrs={'data-testid': 'prism-inline-image'}).find('img')['src']
            except AttributeError:
                image_link = 'none'
            except TypeError:
                image_link = 'none'

            try:
                a_list = [i.text for i in html.find('div', attrs={'data-testid': 'prism-byline'}).find_all('span')]
                article_author = ""

                for string in a_list:
                    article_author += string + " "

            except AttributeError:
                article_author = 'none'
            except TypeError:
                article_author = 'none'

            try:
                publish_date = html.find('div', attrs={'class': 'VZTD '}).find("div").text.strip()
            except AttributeError:
                publish_date = 'none'
            except TypeError:
                publish_date = 'none'

            image_links[number] = image_link

            article_details[number] = [article_link[1],
                                       (f'{IMAGE_DIRECTORY}\\{number}ABC.jpg' if image_link != 'none' else 'none'),
                                       (article_link[0] if article_link[0] != 'none' else 'none'), article_author,
                                       publish_date,
                                       article_link[2], LOGO]
    except Exception:
        pass

    return article_details
