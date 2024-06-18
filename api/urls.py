from django.contrib import admin
from django.urls import path
 
from . import views
 
app_name = 'api'
 
urlpatterns = [
    path('user/', views.UserView.as_view(), name='user_data'),
]
 