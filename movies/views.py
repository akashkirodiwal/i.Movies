from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie, Screening


# Create your views here.

def booking(request):
    context = {'movies': Movie.objects.all()}
    return render(request, 'movies/booking.html', context)


def movie_selected(request,movie_title):

    context = {'screening': Screening.objects.filter(movie_id__title__contains=movie_title)}
    return render(request, 'movies/screening.html', context)
