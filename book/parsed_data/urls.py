
from django.conf.urls import url
from . import views
from django.urls import path
urlpatterns = [
   path('kyobo/', views.kyobo, name="kyobo_book"),
   path('aladin/', views.aladin, name="aladin_book"),
   path('yes24/', views.yes24, name="yes24_book"),
   path('', views.main, name="main"),
]
