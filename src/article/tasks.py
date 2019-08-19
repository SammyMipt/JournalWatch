from celery import task
from habanero import Crossref
import validators


@task(bind=True, time_limit=3000, default_retry_delay=60, max_retries=5, soft_time_limit=10000)
def async_post_save_article_info(self, doi):

    from .models import Article
    from .signals import get_abstract, get_image_url

    article = Article.objects.get(DOI=doi)

    if not article.image_url and not article.abstract:
        cr = Crossref()
        article_meta = cr.works(ids=article.DOI)
        article.abstract = get_abstract(article_meta)
        article.image_url = get_image_url(article_meta)

        if not validators.url(article.image_url):
            article.image_url = str()

        article.save()
