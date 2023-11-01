from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("get_data/", views.get_data, name="get_data"),
    path('restaurant/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path("", views.RestaurantsView.as_view(), name="index"),
    path("restaurant/<int:pk>/add_review", views.add_review, name="add_review"),
    path('<int:pk>/myvotes/', views.MyReviews.as_view(), name='my_reviews'),
    path('filter/', views.GetRestaurantByCategoryAndState.as_view(), name='filtered_category_state'),
]