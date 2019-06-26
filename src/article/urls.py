from django.urls import path
from .views import *


urlpatterns = [
    path(r'', AddArticle.as_view(), name='add_article'),
]
