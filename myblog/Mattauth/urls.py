from django.urls import path
from . import views

app_name = 'Mattauth'

urlpatterns = [
    path('login', views.Mylogin, name='login'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='email_captcha'),
    path('logout', views.Mylogin, name='logout')
    
]