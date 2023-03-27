import asyncio
import os.path
import time
import requests
from bs4 import BeautifulSoup as bS
from src.image_downloader import download_images_async
from tqdm import tqdm

# request the wall street journal  website
WEBSITE_LINK = 'https://www.nytimes.com/international/section/climate'
WEBSITE = bS(requests.get(WEBSITE_LINK).content, "html.parser")
IMAGE_DIRECTORY = "NYT\\"
LOGO = os.path.join("Assets", "NYT-Logo.png")

# this storage will hold the articles of wall st in format :
# [['headline_text', 'image_path', 'article_link', 'publish_date', author_name, 'excerpt']

target_number_of_articles = 5  # number of max articles to find
article_details = []
image_links = []  # stores the links for the images

highlight_articles = bS.find(WEBSITE, 'section', attrs={'id': 'collection-highlights-container'}).find('div').find_all('article', limit=5)
latest_articles = []

# if the articles found on the highlight section is less than the target number of articles
if len(highlight_articles) < target_number_of_articles:
    latest_articles = [x.find('div') for x in bS.find(WEBSITE, 'section', attrs={'id': 'stream-panel'}).find('ol').find_all('li', limit=(target_number_of_articles - len(highlight_articles)))]


async def scrape():
    if not os.path.exists(IMAGE_DIRECTORY): # ensures that the folder for the images are existent
        os.mkdir(IMAGE_DIRECTORY)

    number = 0
    for article in highlight_articles:  # scrapes all the articles in the hight_light section of NYT
        headline_text = article.find('div', attrs={'class': 'css-10wtrbd'}).find('h2').find('a').text

        try:
            article_link = "https://www.nytimes.com" + article.find('div', attrs={'class': 'css-10wtrbd'}).find('h2').find('a')['href']
        except TypeError:
            continue
        except AttributeError:
            continue

        try:
            image_link = article.find('figure').find('img')['src']
        except TypeError:
            image_link = 'none'
        except AttributeError:
            image_link = 'none'

        try:
            excerpt = article.find('p', attrs={'class': 'css-tskdi9 e1hr934v4'}).text
        except AttributeError:
            excerpt = 'none'
        except TypeError:
            excerpt = 'none'

        try:
            author_name = article.find('span', attrs={'itemprop': 'name'}).text
        except AttributeError:
            author_name = 'none'
        except TypeError:
            author_name = 'none'

        try: # can't find the publish date unless i reach the article inside
            publish_date = article.find('span', attrs={'data-testid': 'todays-date'}).text
        except AttributeError:
            publish_date = 'none'
        except TypeError:
            publish_date = 'none'

        image_links.append(image_link)

        article_details.append([headline_text, (f'{IMAGE_DIRECTORY}\\{number}NYT.jpg'
                                                if image_link != 'none' else 'none'),
                                article_link, publish_date, author_name, excerpt, LOGO])

        number += 1

    for article in latest_articles: # scrapes all the articles in the latest_articles in new york times
        headline_text = article.find('a').find('h2').text

        try:
            article_link = "https://www.nytimes.com" + article.find('a')['href']
        except TypeError:
            continue
        except AttributeError:
            continue

        try:  # produces a low quality image
            image_link = article.find('figure').find('img')['src']
        except TypeError:
            image_link = 'none'
        except AttributeError:
            image_link = 'none'

        try:
            excerpt = article.find('a').find('p').text
        except AttributeError:
            excerpt = 'none'
        except TypeError:
            excerpt = 'none'

        try:
            author_name = article.find('div', attrs={'class': 'e15t083i3'}).find('span').text
        except AttributeError:
            author_name = 'none'
        except TypeError:
            author_name = 'none'

        try:
            publish_date = article.find('span', attrs={'class': 'css-1n7hynb'}).text
        except AttributeError:
            publish_date = 'none'
        except TypeError:
            publish_date = 'none'

        image_links.append(image_link)

        article_details.append(
            [headline_text, (f'{IMAGE_DIRECTORY}\\{number}NYT.jpg' if image_link != 'none' else 'none'),
             article_link, publish_date, author_name, excerpt, LOGO])

        number += 1

    await download_images_async(image_links, IMAGE_DIRECTORY, 'NYT.jpg')

    return article_details


def display_details():  # for testing.
    i = 0
    for article in article_details:
        print("Headline: " + article[0])
        print("Image: " + image_links[i])
        print("Link: " + article[2])
        print("Author: " + article[3])
        print("Data Published: " + article[4])
        print("Summary: " + article[5] + "\n")
        i += 1


def run():  # for testing. call on the main function to use
    start = time.time()
    asyncio.run(scrape())
    print(f'finished in {time.time() - start}')

