from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q

from .models import Article


class AddArticle(CreateView):
    model = Article
    template_name = 'article/add_article.html'
    fields = ('DOI', 'theme', "article_file", )

    def form_valid(self, form):
        return super(AddArticle, self).form_valid(form)

    def get_success_url(self):
        return ""
