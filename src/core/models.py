from django.db import models


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField("email address", blank=False, unique=True, null=True)

    def __str__(self):
        return self.username

    def get_pubs(self):
        return self.articles

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Dated(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')

    class Meta:
        verbose_name = 'Dated'
        verbose_name_plural = 'Dated'
        abstract = True

