from bs4 import BeautifulSoup
import requests
import re


aps_url_base = "https://journals.aps.org"


def clean_html(raw_html):
    clean_re = re.compile('<.*?>')
    clean_text = re.sub(clean_re, '', raw_html)
    return clean_text


def get_aps_abstract(url):
    full_html = requests.get(url).text
    soup = BeautifulSoup(full_html, features="html.parser")
    soup = soup.find(class_="article open abstract")
    soup = soup.find(class_="content")
    soup = soup.find("p")
    return clean_html(str(soup)).encode("unicode_escape").decode('utf-8')


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
