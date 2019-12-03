
from django.conf.urls import url
from . import views
from django.urls import path
urlpatterns = [
   path('', views.book),
   path('select/', views.select, name="select"),
]
