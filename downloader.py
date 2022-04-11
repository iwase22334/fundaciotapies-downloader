#!/usr/bin/env python3
import time
import requests
import re
import tqdm
from bs4 import BeautifulSoup

base_url = "https://fundaciotapies.org/en/the-collection/selected-works/?pg=%d"
collection_urls = [
    base_url % i
    for i in range(1, 11)
]


def parse_collection_page(url):
    urls = []

    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    for image_container in soup.find_all("div", {"class": "image-container"}):
        title = image_container.parent.find("h6").text

        style = image_container.get("style")
        image_url = re.match(r".*url\((.*)\)", style).group(1)

        assert image_url
        urls.append((title, image_url))

    return urls


def to_filepath(title):
    author = "Antoni Tàpies"
    file_name = author + " - " + title + ".jpg"
    file_name = file_name.replace(" ", "_")

    # Remove bad path chars
    file_name = re.sub(r'[^\w\-_\. ]', '_', file_name)
    return file_name


def download_image_as(path, url):
    image = requests.get(url).content
    with open(path, "wb") as f:
        f.write(image)


if __name__ == "__main__":

    for collection_url in tqdm.tqdm(collection_urls):
        print("Current index page url: " + collection_url)
        image_urls = parse_collection_page(collection_url)

        for title, image_url in image_urls:
            print("Downloading:", title + "<" + image_url + ">")
            download_image_as(to_filepath(title), image_url)
            print("Complete:", to_filepath(title))

            time.sleep(0.2)
