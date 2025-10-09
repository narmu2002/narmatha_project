from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('about/', views.about, name='about'),
     path('contact/', views.contact, name='contact'),
     path('registration/', views.registration, name='registration'),
     path('form/',views.display_form, name='form'),
     path('mail', views.mail_send, name='mail'),
      path('password',views.gen_pass, name='genpass'),
      path('logout/', views.logout_view, name='logout'),
      path('signup/', views.sign, name='signup'),
    path('set-password/', views.set_new_password, name='set_new_password'),
    path('verify/', views.verify_temp_password, name='verify'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
     
]
