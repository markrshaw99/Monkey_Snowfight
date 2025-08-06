from django.urls import path
from monkeyhome.views import *

urlpatterns = [
    path('', home_view, name="home"),  
]
