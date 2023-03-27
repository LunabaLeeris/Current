import asyncio
import os.path
import time
import requests
from bs4 import BeautifulSoup as bS
from src.image_downloader import download_images_async
from tqdm import tqdm

# request the vox website
WEBSITE_LINK = "https://www.vox.com/energy-and-environment"
WEBSITE = bS(requests.get(WEBSITE_LINK).content, "html.parser")
LOGO = os.path.join("Assets", "VOX-Logo.png")
IMAGE_DIRECTORY = "VoxImages\\"  # file directory where the images will be stored

# this storage will hold the articles of vox in format:
# [['headline_text', 'image_path', 'article_link', 'article_author', 'publish_date', excerpt]

article_details = []

image_links = []  # stores the links for the images

articles = bS.find_all(WEBSITE, "div", attrs={'class': "c-compact-river__entry"},
                       limit=5)  # finds only 5 article in the vox. Can be changed to increase the size


async def scrape():  # main important function
    # checks whether a directory exists
    if not os.path.exists(IMAGE_DIRECTORY):
        os.mkdir(IMAGE_DIRECTORY)

    number = 0  # responsible for naming the images
    for article in articles:
        # gets the link of the article inside the image
        image_wrapper = article.find("div").find("a", attrs={'class': 'c-entry-box--compact__image-wrapper'})
        try:
            article_link = image_wrapper['href']  # gets the reference link on the image wrapper
        except TypeError:
            continue
        except AttributeError:
            continue

        #  goes inside the div to get the headline text
        headline_text = article.find("div").find("div", attrs={'class': 'c-entry-box--compact__body'})\
            .find('h2', attrs={'class': 'c-entry-box--compact__title'}).text

        # goes inside the image wrapper to get the image link
        try:
            image_link = \
            image_wrapper.find('div', attrs={'class': 'c-entry-box--compact__image'}).find('noscript').find('img')['src']
        except TypeError:
            image_link = 'none'
        try:
            article_author = article.find('span', attrs={'class': 'c-byline__author-name'}).text
        except AttributeError:
            article_author = 'none'

        try:
            publish_date = article.find('time', attrs={'time': 'c-byline__item'}).text
        except AttributeError:
            publish_date = 'none'

        # adds the image link to the collection of links to be downloaded later
        image_links.append(image_link)

        article_details.append([headline_text, IMAGE_DIRECTORY + (f'{number}VOX.jpg' if image_link !=
                                                                                        'none' else 'none'),
                                article_link, article_author, publish_date, "none", LOGO])

        number += 1

    # downloads the images found on the links asynchronously for faster performance
    await download_images_async(image_links, IMAGE_DIRECTORY, 'VOX.jpg')

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
    display_details()
    print(f'finished in {time.time() - start}')

