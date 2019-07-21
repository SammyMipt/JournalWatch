from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from habanero import Crossref
from datetime import datetime
from urllib import request
import re
import os

from .models import Article
from .excluded_publishers import publishers
from .excluded_publishers_info import get_aps_abstract, get_aps_image_url


def clean_html(raw_html):
    clean_re = re.compile('<.*?>')
    clean_text = re.sub(clean_re, '', raw_html)
    return clean_text


@receiver(post_save, sender=Article, dispatch_uid="add_article")
def pre_save_article(sender, instance, **kwargs):
    try:
        if not instance.image_file and not instance.image_url:
            print("save")
            cr = Crossref()
            article_meta = cr.works(ids=instance.DOI)
            instance.DOI = instance.DOI.strip()
            instance.abstract = get_abstract(article_meta)
            instance.title = get_title(article_meta)
            instance.description = get_description(article_meta)
            instance.keywords = get_keywords(article_meta)
            instance.article_url = get_url(article_meta)

            if not instance.image_file:
                instance.image_url = get_image_url(article_meta)

    except Exception as e:
        print('%s (%s)' % (str(e), type(e)))


def get_abstract(article_meta):
    abstract = str()
    if "abstract" in article_meta["message"]:
        abstract = clean_html(article_meta["message"]["abstract"])
    elif "publisher" in article_meta["message"] and\
            article_meta["message"]["publisher"].lower() in publishers:
        abstract = get_publishers_abstract(article_meta["message"]["publisher"].lower(), article_meta)
    return abstract.strip()


def get_publishers_abstract(publisher, article_meta):
    if publisher == publishers[0]:
        return clean_html(get_aps_abstract(get_url(article_meta)))
    else:
        return ""


def get_image_url(article_meta):
    abstract = str()
    if "abstract" in article_meta["message"]:
        abstract = clean_html(article_meta["message"]["abstract"])
    elif "publisher" in article_meta["message"] and\
            article_meta["message"]["publisher"].lower() in publishers:
        abstract = get_publishers_image_url(article_meta["message"]["publisher"].lower(), article_meta)
    return abstract.strip()


def get_publishers_image_url(publisher, article_meta):
    if publisher == publishers[0]:
        return clean_html(get_aps_image_url(get_url(article_meta)))
    else:
        return ""


def get_title(article_meta):
    title = str()
    if "title" in article_meta["message"]:
        if len(article_meta["message"]["title"]) > 0:
            title = article_meta["message"]["title"][0]
    return title.strip()


def get_description(article_meta):
    description = str()
    if "author" in article_meta["message"]:
        for author in article_meta["message"]["author"]:
            description += "{0} {1}, ".format(author["given"], author["family"])

        time = str()
        if "created" in article_meta["message"]:
            if "timestamp" in article_meta["message"]["created"]:
                time = datetime.fromtimestamp(article_meta["message"]["created"]["timestamp"] / 1000)\
                                                                                .strftime("%d %B %Y")
        description += "{0} - Published {1}".format(article_meta["message"]["DOI"], time)
    return description.strip()


def get_keywords(article_meta):
    keywords = str()
    if "subject" in article_meta["message"]:
        keywords = "Keywords: "
        for keyword in article_meta["message"]["subject"]:
            keywords += "{0}, ".format(keyword)
    return keywords.strip()[:-1]


def get_url(article_meta):
    url = str()
    if "URL" in article_meta["message"]:
        url = article_meta["message"]["URL"]
    elif "link" in article_meta["message"]:
        if len(article_meta["message"]["link"]) > 0:
            if "URL" in article_meta["message"]["link"][0]:
                url = article_meta["message"]["link"][0]["URL"]
    return url
