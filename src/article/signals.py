from django.db.models.signals import pre_save
from .models import Article
from django.dispatch import receiver
from habanero import Crossref
import re
from datetime import datetime


def clean_html(raw_html):
    clean_re = re.compile('<.*?>')
    clean_text = re.sub(clean_re, '', raw_html)
    return clean_text


@receiver(pre_save, sender=Article, dispatch_uid="update_stock_count")
def pre_save_article(sender, instance, **kwargs):
    try:
        instance.DOI = instance.DOI.strip()
        cr = Crossref()
        article_meta = cr.works(ids=instance.DOI)
        instance.abstract = get_abstract(article_meta)
        instance.title = get_title(article_meta)
        instance.description = get_description(article_meta)
        instance.keywords = get_keywords(article_meta)
        instance.article_url = get_url(article_meta)
    except Exception as e:
        print('%s (%s)' % (str(e), type(e)))


def get_abstract(article_meta):
    abstract = str()
    if "abstract" in article_meta["message"]:
        abstract = clean_html(article_meta["message"]["abstract"])
    return abstract.strip()


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
