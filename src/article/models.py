from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib import request

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
    image_file = models.ImageField(upload_to=u'images/', null=True, blank=True)
    image_url = models.URLField(max_length=1023, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE, null=True,
                               blank=False)

    def save(self, *args, **kwargs):
        super(Article, self).save()

        if self.image_url and not self.image_file:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(request.urlopen(self.image_url).read())
            img_temp.flush()
            self.image_url = ''
            self.image_file.save(self.DOI, File(img_temp))

    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'статьи'
