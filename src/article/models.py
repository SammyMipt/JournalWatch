from django.db import models
from core.models import Dated
from .themes import *


class Article(Dated):
    DOI = models.CharField(max_length=255)
    theme = models.CharField(max_length=255, choices=THEME_CHOICES, default=UNCLASSIFIED)
    title = models.TextField(null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    article_file = models.FileField(upload_to=u'articles/', null=True, blank=True)
    article_url = models.URLField(max_length=1023)

    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'статьи'


class Image(Dated):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image_file = models.FileField(upload_to=u'images/', null=True, blank=False)

    class Meta:
        verbose_name = u'картинка'
        verbose_name_plural = u'картинки'
