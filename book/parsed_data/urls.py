
from django.conf.urls import url
from . import views
from django.urls import path
urlpatterns = [
   path('kyobo/', views.kyobo, name="kyobo_book"),
   path('', views.main, name="main"),
]
