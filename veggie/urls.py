from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("", views.RestaurantsView.as_view(), name="index"),
    path("<str:category_name>/filtered-category/", views.GetRestaurantByCategory.as_view(), name="filtered-category"),
    path("<str:state_name>/filtered-state/", views.GetRestaurantByState.as_view(), name="filtered-state"),
    path("home/", views.home, name="home")
]