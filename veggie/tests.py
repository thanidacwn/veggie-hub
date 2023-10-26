from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .views import RestaurantsView
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
        self.credentials = {
            'username': 'test_user',
            'password': 'secret_password'
        }
        self.user = User.objects.create_user(**self.credentials)

    def test_user_login_redirect(self):
        self.client.login(username='test_user', password='secret_password')
        response = self.client.get(reverse("veggie:index"))
        self.assertEqual(response.status_code, 200)

    def test_user_logout_redirect(self):
        self.client.logout()
        response = self.client.get(reverse("veggie:index"))
        self.assertEqual(response.status_code, 200)

    
class RestaurantViewTest(TestCase):
    def test_template_used_of_homepage(self):
        response = self.client.get(reverse('veggie:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'veggie/home.html')
