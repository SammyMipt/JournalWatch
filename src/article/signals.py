from django.db.models.signals import pre_save
from .models import Article
from django.dispatch import receiver


@receiver(pre_save, sender=Article, dispatch_uid="update_stock_count")
def pre_save_article(sender, instance, **kwargs):
    try:
        print("hello")
        instance.abstract = "lol"
        instance.title = "lol"
        instance.save()
        print("hello")
    except Exception:
        print("error")
