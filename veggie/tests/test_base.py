from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from veggie.models import Category, State, Restaurant, Review
from veggie.forms import ReviewForm


def create_restaurant(restaurant_text):
    """Create a restaurant with given text"""
    category = Category.objects.create(category_text="Test Category")
    state = State.objects.create(state_text="Test State")
    return Restaurant.objects.create(
        restaurant_text=restaurant_text,
        category=category,
        state=state,
        city="Test City",
        location="Test Location",
        restaurant_link="https://example.com/restaurant",
        menu_link="https://example.com/menu",
        price_rate="expensive"
    )

def create_review(restaurant, review_user, review_title, review_description, review_rate):
    """Create a review with given text"""
    return Review.objects.create(
        restaurant=restaurant,
        review_user=review_user,
        review_title=review_title,
        review_description=review_description,
        review_rate=review_rate
    )


def create_user(self):
    """Create a user only if it doesn't already exist."""
    user, _ = User.objects.get_or_create(username='testuser')
    return user