from django.db import models
from django.conf import settings

from core.models import Dated
from .themes import *


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

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return str(self.title) if self.title else ""
