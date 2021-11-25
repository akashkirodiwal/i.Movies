from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Movie, Screening
from users_profile.models import Ticket
from django.contrib.auth.models import User
from users_profile import views as user_views
from django.contrib import messages


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

def payment_status(request):
    messages.success(request,f'Payment Done Successfully')
    return render(request,'movies/payment_done.html')
    
def booked_history(request):
    current_user = request.user
    context={"ticket": Ticket.objects.filter(username=current_user)}
    return render(request,'users_profile/profile.html',context)


def cancel(request, ticket_pk):
    context = {'ticket': Ticket.objects.filter(pk=ticket_pk).first()}
    return render(request, 'movies/cancel.html', context)


def done_cancellation(request, ticket_pk):
    if request.method == 'POST':
        tickets_cancel = request.POST['ticket_cancel']
        current_user = request.user
        user = User.objects.filter(username=current_user).first()
        ticket = Ticket.objects.filter(pk=ticket_pk).first()
        ticket.no_of_seats -= int(tickets_cancel)
        ticket.screening.available_seats += int(tickets_cancel)
        ticket.screening.save()
        ticket.save()
        if ticket.no_of_seats == 0:
            ticket.delete()
        context = {'tickets': Ticket.objects.filter(user=user)}
    return render(request, 'users_profile/profile.html', context)

