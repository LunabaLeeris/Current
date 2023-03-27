import requests  # imports the requests library
from bs4 import BeautifulSoup as bS  # imports the beautiful soup library

WEBSITE_LINK = "link"  # website's link
WEBSITE = bS(requests.get(WEBSITE_LINK).content, "html.parser")  # parses the html content
IMAGE_DIRECTORY = "Directory\\"  # file directory where the images will be stored

# this storage will hold the articles of vox in format:
article_details = []
# [['headline_text', 'image_path', 'article_link', 'article_author', 'publish_date', excerpt]

image_links = []  # stores the links for the images


async def scrape():  # makes the function asynchronous
    # scrapes the important data to be stored on the created lists
    pass
