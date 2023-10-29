from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("home/", views.home, name="home"),
    path('restaurant/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path("", views.RestaurantsView.as_view(), name="index"),
    path("restaurant/<int:restaurant_id>/add_review", views.add_review, name="add_review"),
    path('filter/', views.GetRestaurantByCategoryAndState.as_view(), name='filtered_category_state'),
]