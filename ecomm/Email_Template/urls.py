from django.urls import path
from .views import *
urlpatterns = [
    # path('',home,name='homepage'),
    path('mails/',send_mails,name='mail'),
]