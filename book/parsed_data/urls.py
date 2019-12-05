
from django.conf.urls import url
from . import views
from django.urls import path
urlpatterns = [
   path('kyobo/', views.kyobo_book, name="kyobo_book"),
   path('select/', views.select, name="select"),
   path('', views.kyobo_book),
]
