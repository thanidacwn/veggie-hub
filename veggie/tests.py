from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Category, State, Restaurant, Review


class RestaurantModelTest(TestCase):
    """Test Restaurant model"""
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(category_text="Test Category")
        self.state = State.objects.create(state_text="Test State")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.restaurant = Restaurant.objects.create(
            restaurant_text="Test Restaurant",
            category=self.category,
            state=self.state,
            city="Test City",
            location="Test Location",
            restaurant_link="https://example.com/restaurant",
            menu_link="https://example.com/menu",
            price_rate="expensive"
        )
        self.review = Review.objects.create(
            restaurant=self.restaurant,
            review_user=self.user,
            review_title="Test Review",
            review_description="This is a test review.",
            review_rate=4
        )
        self.review2 = Review.objects.create(
            restaurant=self.restaurant,
            review_user=self.user,
            review_title="Test Review 2",
            review_description="This is a test review 2.",
            review_rate=3
        )
        self.review3 = Review.objects.create(
            restaurant=self.restaurant,
            review_user=self.user,
            review_title="Test Review 3",
            review_description="This is a test review 3.",
            review_rate=1
        )

    def test_average_rate(self):
        """Test average rate"""
        self.assertEqual(self.restaurant.get_average_rate, 2.67)

    def test_reviews_amount(self):
        """Test reviews amount"""
        self.assertEqual(self.restaurant.get_reviews_amount, 3)


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_login_redirect(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("veggie:index"))
        self.assertEqual(response.status_code, 200)


class RestaurantDetailViewTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(category_text="Test Category")
        self.state = State.objects.create(state_text="Test State")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.restaurants = []
        restaurant1 = Restaurant.objects.create(
            restaurant_text="Test Restaurant",
            category=self.category,
            state=self.state,
            city="Test City",
            location="Test Location",
            restaurant_link="https://example.com/restaurant",
            menu_link="https://example.com/menu",
            price_rate="expensive"
        )
        self.review = Review.objects.create(
            restaurant=restaurant1,
            review_user=self.user,
            review_title="Test Review",
            review_description="This is a test review.",
            review_rate=4
        )
        self.review2 = Review.objects.create(
            restaurant=restaurant1,
            review_user=self.user,
            review_title="Test Review 2",
            review_description="This is a test review 2.",
            review_rate=3
        )
        self.review3 = Review.objects.create(
            restaurant=restaurant1,
            review_user=self.user,
            review_title="Test Review 3",
            review_description="This is a test review 3.",
            review_rate=1
        )
        restaurant2 = Restaurant.objects.create(
            restaurant_text="Test Restaurant2",
            category=self.category,
            state=self.state,
            city="Test City",
            location="Test Location",
            restaurant_link="https://example.com/restaurant",
            menu_link="https://example.com/menu",
            price_rate="expensive"
        )
        self.restaurants.append(restaurant1)
        self.restaurants.append(restaurant2)

    def test_detail_view_successfully_show_requested_restaurant(self):
        """Test if detail view show correct requested restaurant"""
        response = self.client.get(reverse('veggie:detail', args=(self.restaurants[0].id,)))
        self.assertEqual(response.context['restaurant'], self.restaurants[0])

    def test_detail_view_give_404_error_message_when_requesting_not_exist_restaurant(self):
        """Test if detail view show error for non-existed requested restaurant will redirect user to index page"""
        non_existed_restaurant_id = 9999
        response = self.client.get(reverse('veggie:detail', args=(non_existed_restaurant_id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('veggie:index'))

    def test_detail_show_all_review_that_requested_restaurant_have(self):
        """Test if detail view show all restaurant's reviews"""
        response = self.client.get(reverse('veggie:detail', args=(self.restaurants[0].id,)))
        self.assertQuerysetEqual(response.context['reviews'],
                                 Review.objects.filter(restaurant=self.restaurants[0].id), ordered=False)

    def test_detail_view_requested_restaurant_has_no_reviews(self):
        """Test if detail view handle requested restaurant has no reviews"""
        response = self.client.get(reverse('veggie:detail', args=(self.restaurants[1].id,)))
        self.assertQuerysetEqual(list(response.context['reviews']), [], ordered=False)
        self.assertEqual(self.restaurants[1].get_reviews_amount, 0)
