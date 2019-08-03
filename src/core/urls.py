from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from application.settings import LOGIN_URL

urlpatterns = [
    path(r'logout/', login_required(LogoutView.as_view(), login_url=LOGIN_URL), name='logout'),
    path(r'login/', LoginView.as_view(), name='login'),
]