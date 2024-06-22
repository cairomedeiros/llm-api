from django.contrib import admin
from django.urls import path

from .views import UserView
from .views import OpenAIAPIView
 
app_name = 'api'
 
urlpatterns = [
    path('user/', UserView.as_view(), name='user_data'),
    path('assistant/', OpenAIAPIView.as_view(), name='openai_data'),
]
 