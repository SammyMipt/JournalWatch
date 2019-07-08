from django.apps import AppConfig


class ArticleConfig(AppConfig):
    name = 'article'

    def ready(self):
        from . import signals