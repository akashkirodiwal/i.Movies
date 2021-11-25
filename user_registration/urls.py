"""user_registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users_profile import views as user_views
from movies import views as mov_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users_profile.urls')),
    path('profile/',user_views.profile,name='profile'),
    path('login/',auth_views.LoginView.as_view(template_name='users_profile/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users_profile/logout.html'),name='logout'),
    path('register/',user_views.register,name='register'),
    path('booking/',mov_views.booking,name='mov_booking'),
    path(r'^screening/(?P<movie_title>.+)/$', mov_views.movie_selected, name='screening'),
    path(r'^booked/(?P<screen_pk>.+?)/$', mov_views.ticket_booked, name='finalbook'),
    path('payment_done/',mov_views.payment_status,name='payment_status'),
    path(r'^cancel/(?P<ticket_pk>.+?)/$', mov_views.cancel, name='cancel'),
    path(r'^done_cancellation/(?P<ticket_pk>.+?)/$', mov_views.done_cancellation, name='done_cancellation'),
    path('otp/<username>/<email>/',user_views.otp,name='otp'),
    path('validate_otp/',user_views.validate_otp,name='validate_otp'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users_profile/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users_profile/password_reset_done.html'),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users_profile/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users_profile/password_reset_complete.html'
         ),
         name='password_reset_complete'),        
            ]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
