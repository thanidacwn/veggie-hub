from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Category, State, Restaurant, Review
from .forms import ReviewForm


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


def create_restaurant(restaurant_text):
    

class AddReviewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('testpass')
        self.user.save()
        self.client.login(username='testuser', password='testpass')

    def test_add_review_is_valid(self):
        """Test add review form is valid"""
        form = ReviewForm(data={'review_title': "Test Review",
                                'review_description': "This is a test review.",
                                'review_rate': 4})
        self.assertTrue(form.is_valid())

    def test_can_review_is_authenticated(self):
        """If user is already logged in, they can review"""
        restaurant = create_restaurant("")
        response = self.client.get(reverse('veggie:add_review', kwargs={'pk': restaurant.pk}))
        self.assertEqual(response.status_code, 200)

class DeleteReviewViewTest(TestCase):
    def setUp(self):
        pass

    def test_delete_review(self):
        pass

    def test_can_not_delete_review_if_not_logged_in(self):
        pass
    def test_can_not_delete_review_if_not_review_user(self):
        pass
