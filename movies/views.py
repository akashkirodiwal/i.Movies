from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Movie, Screening
from users_profile.models import Ticket
from django.contrib.auth.models import User
from users_profile import views as user_views
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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
    current_user=request.user
    us= User.objects.filter(username=current_user).first()
    ticket=Ticket.objects.filter(user=us).last()
    invoice_details={'movie':ticket.screening.movie_id.title,
                      'duration':ticket.screening.movie_id.duration_min,
                      'description':ticket.screening.movie_id.description,
                      'theater':ticket.screening.theatre_id.name,
                      'city':ticket.screening.theatre_id.city,
                      'seats':ticket.no_of_seats,
                      'cost':ticket.cost,
                      'username':current_user,
                      "Date_and_Time":ticket.screening.time
                    }
    email = us.email        
    subject, from_email, to = 'Booking Confirmed', 'aduser.movie30@gmail.com', email
    html_content = render_to_string('movies/invoice_mail.html',invoice_details)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()        
    messages.success(request,f'Payment Done Successfully.\n Invoice sent to your registered email')
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
        ##cancelling Email
        invoice_details={'movie':ticket.screening.movie_id.title,
                      'duration':ticket.screening.movie_id.duration_min,
                      'description':ticket.screening.movie_id.description,
                      'theater':ticket.screening.theatre_id.name,
                      'city':ticket.screening.theatre_id.city,
                      'seats':int(tickets_cancel),
                      'username':user
                    }
        email = user.email        
        subject, from_email, to = 'Booking Cancelled', 'aduser.movie30@gmail.com', email
        html_content = render_to_string('movies/cancel_mail.html',invoice_details)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request,f'Ticket has been Cancelled!!')
        ticket.no_of_seats -= int(tickets_cancel)
        ticket.screening.available_seats += int(tickets_cancel)
        ticket.screening.save()
        ticket.save()

        if ticket.no_of_seats == 0:
            ticket.delete()
        context = {'tickets': Ticket.objects.filter(user=user)}
        
    return render(request, 'users_profile/home.html', context)

