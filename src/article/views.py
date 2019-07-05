from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q

from .models import Article
from .forms import AddingForm, GettingForm


class AddArticle(CreateView):
    model = Article
    template_name = 'article/add_article.html'
    form_class = AddingForm
    success_url = 'add_article'

    def get_success_url(self):
        return reverse(self.success_url)


class GetArticles(ListView):
    model = Article
    template_name = 'article/get_article.html'
    form_class = GettingForm
    success_url = 'get_article'
    fields = ('created_at_start',)

    def get_success_url(self):
        return reverse(self.success_url)