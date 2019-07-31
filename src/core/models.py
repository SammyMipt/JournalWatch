from django.db import models


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def __str__(self):
        return self.username

    # def get_absolute_url(self):
    #     from django.urls import reverse
    #     return reverse('core:user', kwargs={'slug': self.username})

    def get_pubs(self):
        return self.articles

    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'


class Dated(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'дата создания')

    class Meta:
        verbose_name = u'датированный'
        verbose_name_plural = u'датированные'
        abstract = True

