from bs4 import BeautifulSoup
import requests


aps_url_base = "https://journals.aps.org"


def get_aps_abstract(url):
    full_html = requests.get(url).text
    soup = BeautifulSoup(full_html, features="html.parser")
    soup = soup.find(class_="article open abstract")
    soup = soup.find(class_="content")
    soup = soup.find("p")
    return str(soup)


def get_aps_image_url(url):
    full_html = requests.get(url).text
    soup = BeautifulSoup(full_html, features="html.parser")
    soup = soup.find(class_="article open abstract")
    soup = soup.find(class_="content")
    soup = soup.find(class_="clear-wrap")
    soup = soup.find("img")
    src = str(soup.attrs["src"])
    pos = src.find("thumbnail")
    src = aps_url_base + src[:pos] + "medium"
    return src
