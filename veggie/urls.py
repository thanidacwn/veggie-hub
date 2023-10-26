from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("", views.index, name="index"),
    # path("home", views.home, name="home")
    path("restaurant/<int:restaurant_id>/add_review", views.add_review, name="add_review"),
    path("", views.RestaurantsView.as_view(), name="index"),
    path('filter/', views.GetRestaurantByCategoryAndState.as_view(), name='filtered_category_state'),
]