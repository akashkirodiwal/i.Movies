from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Ticket
# Create your views here.


def home(request):
    return render(request, 'users_profile/home.html')


def register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {username}.You can Login Now!!')
            return redirect('login')

    else:
        form=UserRegisterForm()
    return render(request,'users_profile/register.html',{'form':form})

@login_required
def profile(request):
    current_user = request.user
    context = {'tickets': Ticket.objects.filter(user=current_user)}
    for ticket in Ticket.objects.filter(user=current_user):
        if ticket.no_of_seats == 0:
            ticket.delete()
    return render(request,'users_profile/profile.html', context)
