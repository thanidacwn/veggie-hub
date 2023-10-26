from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("", views.RestaurantsView.as_view(), name="index"),
    path('filter/', views.GetRestaurantByCategoryAndState.as_view(), name='filtered_category_state'),
    path("home/", views.home, name="home")
]