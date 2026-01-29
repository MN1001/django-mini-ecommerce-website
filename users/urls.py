from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('reg/',views.regview,name='register'),
    path('login/',views.loginview,name='login'),
]