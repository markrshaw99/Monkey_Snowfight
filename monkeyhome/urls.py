from django.urls import path
from monkeyhome.views import *

urlpatterns = [
    path('', welcome, name="welcome"),
]
