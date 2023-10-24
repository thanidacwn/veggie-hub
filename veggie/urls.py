from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("", views.index, name="index"),
    # path("home", views.home, name="home")
    path("add_review/<int:restaurant_id>", views.add_review, name="add_review")
    
]