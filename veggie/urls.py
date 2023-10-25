from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("", views.RestaurantsView.as_view(), name="index"),
    path("<str:category_name>/filtered/", views.GetRestaurantByCategory.as_view(), name="filtered_category"),
    path("home/", views.home, name="home")
]