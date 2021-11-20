from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',
                                                authentication_form=UserLoginForm), name = 'login'),

    path('profile/', views.profile, name='profile')
    
]