from django.urls import path
from .views import *


urlpatterns = [
    path(r'', AddArticle.as_view(), name='add_article'),
    path(r'get/', GetArticles.as_view(), name='get_article'),
    path(r'docx/', get_docx, name='get_docx'),
]
