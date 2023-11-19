from django.contrib import admin
from .models import Category, State, Restaurant, Review, BookMark

admin.site.register([Category, State, Restaurant, Review, BookMark])
