from django.conf.urls import url
from django.urls import path
from .models import Theatre,Movie,Screening
from movies import views as movies_views

urlpatterns = [
    path('', movies_views.booking, name='booking'),
    url(r'^screening/(?P<movie_title>.+?)/$', movies_views.movie_selected, name='screening'),
]
