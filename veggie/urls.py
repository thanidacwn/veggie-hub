from django.urls import path
from . import views

app_name = 'veggie'

urlpatterns = [
    path("get_data/", views.get_data, name="get_data"),
    path('restaurant/<int:pk>/', views.DetailView.as_view(),
         name='detail'),
    path("", views.RestaurantsView.as_view(), name="index"),
    path("restaurant/<int:pk>/add_review", views.add_review,
         name="add_review"),
    path('restaurant/<int:pk>/edit_review', views.edit_review,
         name='edit_review'),
    path('<int:pk>/my_reviews/', views.MyReviews.as_view(),
         name='my_reviews'),
    path('filter/', views.GetRestaurantByCategoryAndState.as_view(),
         name='filtered_category_state'),
    path('<int:pk>/my_reviews/delete/', views.delete_review,
         name="delete"),
    path("<int:pk>/bookmarks/", views.MyBookMarks.as_view(),
         name="my_bookmarks"),
    path('add_bookmark/<int:pk>', views.add_bookmark,
         name='add_bookmark'),
    path('delete_bookmark/<int:pk>', views.delete_bookmark,
         name='delete_bookmark')
]
