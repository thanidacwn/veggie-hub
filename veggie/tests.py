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


class RestaurantIndexViewTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.categories = []
        self.categories.append(Category.objects.create(category_text="TestCategory1"))
        self.categories.append(Category.objects.create(category_text="TestCategory2"))
        self.states = []
        self.states.append(State.objects.create(state_text="TestState1"))
        self.states.append(State.objects.create(state_text="TestState2"))
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.restaurants = []
        restaurant1 = Restaurant.objects.create(
            restaurant_text="TestRestaurant1",
            category=self.categories[0],
            state=self.states[0],
            city="Test City",
            location="Test Location",
            restaurant_link="https://example.com/restaurant1",
            menu_link="https://example.com/menu1",
            price_rate="expensive"
        )
        restaurant2 = Restaurant.objects.create(
            restaurant_text="TestRestaurant2",
            category=self.categories[1],
            state=self.states[1],
            city="Test City",
            location="Test Location",
            restaurant_link="https://example.com/restaurant2",
            menu_link="https://example.com/menu2",
            price_rate="expensive"
        )
        restaurant3 = Restaurant.objects.create(
            restaurant_text="TestRestaurant3",
            category=self.categories[0],
            state=self.states[1],
            city="Test City",
            location="Test Location",
            restaurant_link="https://example.com/restaurant3",
            menu_link="https://example.com/menu3",
            price_rate="expensive"
        )
        self.restaurants.append(restaurant1)
        self.restaurants.append(restaurant2)
        self.restaurants.append(restaurant3)

    def test_show_all_restaurant(self):
        """Test if the application shows all restaurant in the database"""
        response = self.client.get(reverse('veggie:index'))
        self.assertQuerysetEqual(list(response.context['all_restaurants']), self.restaurants, ordered=False)

    def test_show_all_categories(self):
        """Test if the application shows all categories in the database with added 'All' to show all categories"""
        response = self.client.get(reverse('veggie:index'))
        self.assertQuerysetEqual(list(response.context['all_categories']),
                                 ["All", "TestCategory1", "TestCategory2"], ordered=False)

    def test_show_all_states(self):
        """Test if the application shows all states in the database with added 'All' to show all states"""
        response = self.client.get(reverse('veggie:index'))
        self.assertQuerysetEqual(list(response.context['all_states']),
                                 ["All", "TestState1", "TestState2"], ordered=False)

    def test_sort_by_category(self):
        """Test sorting restaurant by category in Home page"""
        base_url = reverse('veggie:filtered_category_state')
        category = 'TestCategory1'
        state = 'All'
        response = self.client.get(f"{base_url}?category={category}&state={state}")
        self.assertQuerysetEqual(list(response.context['all_restaurants']),
                                 [self.restaurants[0], self.restaurants[2]], ordered=False)

    def test_sort_by_state(self):
        """Test sorting restaurant by state in Home page"""
        base_url = reverse('veggie:filtered_category_state')
        category = 'All'
        state = 'TestState2'
        response = self.client.get(f"{base_url}?category={category}&state={state}")
        self.assertQuerysetEqual(list(response.context['all_restaurants']),
                                 [self.restaurants[1], self.restaurants[2]], ordered=False)

    def test_sort_by_both_category_and_state(self):
        """Test sorting restaurant by both category and state in Home page"""
        base_url = reverse('veggie:filtered_category_state')
        category = 'TestCategory1'
        state = 'TestState2'
        response = self.client.get(f"{base_url}?category={category}&state={state}")
        self.assertQuerysetEqual(list(response.context['all_restaurants']), [self.restaurants[2]], ordered=False)
