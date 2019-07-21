from django.apps import AppConfig


class ArticleConfig(AppConfig):
    name = 'article'

    def ready(self):
        from . import signals
        from . import excluded_publishers_info
        from . import excluded_publishers
        from . import themes