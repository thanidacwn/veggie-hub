from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("home", views.home, name="home")
]