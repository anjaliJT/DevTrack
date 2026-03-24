from django.urls import path
from .views import *

urlpatterns = [
    path('reporters/', create_reporter),
    path('reporters/', get_reporters),

    path('issues/', create_issue),
    path('issues/', get_issues),
]