from django.db import models


class Dated(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'дата создания')

    class Meta:
        verbose_name = u'датированный'
        verbose_name_plural = u'датированные'
        abstract = True

