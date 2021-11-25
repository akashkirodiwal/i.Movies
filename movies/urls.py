from django.conf.urls import url
from django.urls import path
from .models import Theatre,Movie,Screening
from movies import views as movies_views

urlpatterns = [
    path('', movies_views.booking, name='booking'),
    url(r'^screening/(?P<movie_title>.+?)/$', movies_views.movie_selected, name='screening'),
    url(r'^booked/(?P<screen_pk>.+?)/$', movies_views.ticket_booked, name='finalbook'),
    path('booked_history/',movies_views.booked_history,name='book_history'),
]
