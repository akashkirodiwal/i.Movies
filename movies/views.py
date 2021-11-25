from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Movie, Screening
from users_profile.models import Ticket
from django.contrib.auth.models import User
from users_profile import views as user_views


# Create your views here.


def booking(request):
    context = {'movies': Movie.objects.all()}
    return render(request, 'movies/booking.html', context)


def movie_selected(request, movie_title):
    context = {'screening': Screening.objects.filter(movie_id__title__contains=movie_title)}
    return render(request, 'movies/screening.html', context)


def ticket_booked(request, screen_pk):
    if request.method == 'POST':
        no_of_seats = request.POST['no_of_seats']
        current_user = request.user
        user = User.objects.filter(username=current_user).first()
        screen = Screening.objects.filter(pk=screen_pk).first()
        screen.available_seats -= int(no_of_seats)
        screen.save()
        
        ticket = Ticket(user=user, screening=screen,no_of_seats=no_of_seats,cost=int(screen.price)*int(no_of_seats))
        ticket.save()
        
        context = {'ticket': ticket}
        
        return render(request,'movies/payment.html',context)
    
def booked_history(request):
    current_user = request.user
    context={"ticket": Ticket.objects.filter(username=current_user)}
    return render(request,'users_profile/profile.html',context)



