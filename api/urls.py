from django.contrib import admin
from django.urls import path

from .views import UserView
from .views import LlamaView
 
app_name = 'api'
 
urlpatterns = [
    path('user/', UserView.as_view(), name='user_data'),
    path('llama/', LlamaView.as_view(), name='llama_data'),
]
 