from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.IndexView.as_view(), name="home")
]
