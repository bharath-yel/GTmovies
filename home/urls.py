from django.urls import path
from . import views
urlpatterns = [
    #path function maps this url to a function in our views file
    path('', views.index, name="home.index"),
    path('about', views.about, name='home.about'),
]