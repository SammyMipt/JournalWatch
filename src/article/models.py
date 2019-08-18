from django.db import models
from django.conf import settings
from habanero import Crossref

import validators

from core.models import Dated
from .themes import *
from .signals import *


class Article(Dated):
    DOI = models.CharField(max_length=191)
    theme = models.CharField(max_length=191, choices=THEME_CHOICES, default=UNCLASSIFIED)
    title = models.TextField(null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    article_url = models.URLField(max_length=1023)
    image_url = models.URLField(max_length=1023, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE, null=True,
                               blank=False)

    def save(self, *args, **kwargs):
        cr = Crossref()
        article_meta = cr.works(ids=self.DOI)
        self.DOI = self.DOI.strip()
        self.abstract = get_abstract(article_meta)
        self.title = get_title(article_meta)
        self.description = get_description(article_meta)
        self.keywords = get_keywords(article_meta)
        self.article_url = get_url(article_meta)
        self.image_url = get_image_url(article_meta)

        if not validators.url(self.image_url):
            self.image_url = ""

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return str(self.title) if self.title else ""
