from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, State, Restaurant, Review


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


def create_review(restaurant, review_user, review_title,
                  review_description, review_rate):
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


class RestaurantModelTest(TestCase):
    """Test Restaurant model"""

    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(category_text="Test Category")
        self.state = State.objects.create(state_text="Test State")
        self.user = User.objects.create_user(username="testuser",
                                             password="testpassword")
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
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)

    def test_user_login_redirect(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("veggie:index"))
        self.assertEqual(response.status_code, 200)


class RestaurantIndexViewTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.categories = []
        self.categories.append(Category.objects.create(
            category_text="TestCategory1"))
        self.categories.append(Category.objects.create(
            category_text="TestCategory2"))
        self.states = []
        self.states.append(State.objects.create(state_text="TestState1"))
        self.states.append(State.objects.create(state_text="TestState2"))
        self.user = User.objects.create_user(username="testuser",
                                             password="testpassword")
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
        self.assertQuerysetEqual(list(response.context['all_restaurants']),
                                 self.restaurants, ordered=False)

    def test_show_all_categories(self):
        """Test if the application shows all categories
        in the database with added 'All' to show all categories"""
        response = self.client.get(reverse('veggie:index'))
        self.assertQuerysetEqual(list(response.context['all_categories']),
                                 ["All", "TestCategory1", "TestCategory2"],
                                 ordered=False)

    def test_show_all_states(self):
        """Test if the application shows all states
        in the database with added 'All' to show all states"""
        response = self.client.get(reverse('veggie:index'))
        self.assertQuerysetEqual(list(response.context['all_states']),
                                 ["All", "TestState1", "TestState2"],
                                 ordered=False)

    def test_sort_by_category(self):
        """Test sorting restaurant by category in Home page"""
        base_url = reverse('veggie:filtered_category_state')
        category = 'TestCategory1'
        state = 'All'
        response = self.client.get(
            f"{base_url}?category={category}&state={state}")
        self.assertQuerysetEqual(list(response.context['all_restaurants']),
                                 [self.restaurants[0], self.restaurants[2]],
                                 ordered=False)

    def test_sort_by_state(self):
        """Test sorting restaurant by state in Home page"""
        base_url = reverse('veggie:filtered_category_state')
        category = 'All'
        state = 'TestState2'
        response = self.client.get(
            f"{base_url}?category={category}&state={state}")
        self.assertQuerysetEqual(
            list(response.context['all_restaurants']),
            [self.restaurants[1], self.restaurants[2]], ordered=False)

    def test_sort_by_both_category_and_state(self):
        """Test sorting restaurant by both category and state in Home page"""
        base_url = reverse('veggie:filtered_category_state')
        category = 'TestCategory1'
        state = 'TestState2'
        response = self.client.get(
            f"{base_url}?category={category}&state={state}")
        self.assertQuerysetEqual(list(response.context['all_restaurants']),
                                 [self.restaurants[2]], ordered=False)


class RestaurantDetailViewTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(category_text="Test Category")
        self.state = State.objects.create(state_text="Test State")
        self.user = User.objects.create_user(username="testuser",
                                             password="testpassword")
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
        response = self.client.get(reverse('veggie:detail',
                                           args=(self.restaurants[0].id,)))
        self.assertEqual(response.context['restaurant'],
                         self.restaurants[0])

    def test_detail_view_error_message_not_exist_restaurant(self):
        """Test if detail view show error for non-existed
        requested restaurant will redirect user to index page"""
        non_existed_restaurant_id = 9999
        response = self.client.get(reverse('veggie:detail',
                                           args=(non_existed_restaurant_id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('veggie:index'))

    def test_detail_show_all_review_that_requested_restaurant_have(self):
        """Test if detail view show all restaurant's reviews"""
        response = self.client.get(reverse('veggie:detail',
                                           args=(self.restaurants[0].id,)))
        self.assertQuerysetEqual(response.context['reviews'],
                                 Review.objects.filter(
            restaurant=self.restaurants[0].id), ordered=False)

    def test_detail_view_requested_restaurant_has_no_reviews(self):
        """Test if detail view handle requested restaurant has no reviews"""
        response = self.client.get(reverse('veggie:detail',
                                           args=(self.restaurants[1].id,)))
        self.assertQuerysetEqual(list(response.context['reviews']),
                                 [], ordered=False)
        self.assertEqual(self.restaurants[1].get_reviews_amount, 0)


class ReviewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('testpass')
        self.other_user, _ = User.objects.get_or_create(
            username='otheruser',
            password='testpassword')
        self.user.save()
        self.client.login(username='testuser', password='testpass')

    def test_add_review_is_valid(self):
        """Test add review, form is valid and after submit,
        review is added. then redirect to restaurant detail page."""
        # Assuming create_restaurant is a valid function
        restaurant = create_restaurant("")
        url = reverse('veggie:add_review', args=(restaurant.id,))
        # check if form is valid
        response = self.client.post(url, {
            'review_title': 'Test Review',
            'review_description': 'This is a test review.',
            'review_rate': 4
        })
        # check if review is added
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('veggie:detail',
                                               args=(restaurant.id,)))
        # review amount is added
        self.assertEqual(restaurant.get_reviews_amount, 1)

    def test_can_review_is_authenticated(self):
        """If user is already logged in, they can add review"""
        restaurant = create_restaurant("")
        response = self.client.get(reverse('veggie:add_review',
                                           args=(restaurant.id,)))
        url = reverse('veggie:add_review', args=(restaurant.id,))
        # check if form is valid
        response = self.client.post(url, {
            'review_title': 'Test Review',
            'review_description': 'This is a test review.',
            'review_rate': 4
        })
        # check if review is added
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('veggie:detail',
                                               args=(restaurant.id,)))
        # review amount is added
        self.assertEqual(restaurant.get_reviews_amount, 1)

    def test_can_not_review_if_not_logged_in(self):
        """If user is not logged in, they can not add review"""
        self.client.logout()
        restaurant = create_restaurant("")
        response = self.client.get(reverse('veggie:add_review',
                                           args=(restaurant.id,)))

        self.assertEqual(response.status_code, 302)
        # check that the user is redirected to the login page
        self.assertIn(reverse('account_login'), response.url)
        # review amount is not added
        self.assertEqual(restaurant.get_reviews_amount, 0)

    def test_can_not_delete_review_if_not_logged_in(self):
        """If user is not logged in, they can not delete review."""
        self.client.logout()
        user = create_user(self)
        restaurant = create_restaurant("")
        review = create_review(restaurant, user, "Test Review",
                               "This is a test review.", 4)
        url = reverse('veggie:delete', args=(review.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # check that the user is redirected to the login page
        self.assertIn(reverse('account_login'), response.url)
        # review amount is not reduced
        self.assertEqual(restaurant.get_reviews_amount, 1)

    def test_can_delete_review_if_reviewed(self):
        """If user is logged in and they have reviewed,
        they can delete review."""
        # Log in the user
        user = create_user(self)
        self.client.force_login(user)
        restaurant = create_restaurant("")
        review = create_review(restaurant, user,
                               "Test Review", "This is a test review.", 4)
        url = reverse('veggie:delete', args=(review.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # check that the user is redirected to the my_reviews page
        self.assertRedirects(response, reverse('veggie:my_reviews',
                                               args=(restaurant.id,)))
        # review amount is reduced
        self.assertEqual(restaurant.get_reviews_amount, 0)
        # assert that the review is deleted
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(pk=review.id)

    def test_review_is_added_to_my_reviews(self):
        """If user already reviewed, it is added to my_reviews page."""
        user = create_user(self)
        self.client.force_login(user)
        restaurant = create_restaurant("")
        review = create_review(restaurant, user,
                               "Test Review", "This is a test review.", 4)
        url = reverse('veggie:my_reviews', args=(restaurant.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # check that the review is in the response
        self.assertContains(response, review.review_title)
        self.assertContains(response, review.review_description)
        self.assertContains(response, review.review_rate)

    def test_review_more_than_one(self):
        """If user already reviewed more than one,
        it is added to my_reviews page."""
        user = create_user(self)
        self.client.force_login(user)
        restaurant = create_restaurant("")
        review = create_review(restaurant, user,
                               "Test Review", "This is a test review.", 4)
        review2 = create_review(restaurant, user,
                                "Test Review 2", "This is a test review 2.", 3)
        url = reverse('veggie:my_reviews', args=(restaurant.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # check that the review is in the response
        self.assertContains(response, review.review_title)
        self.assertContains(response, review.review_description)
        self.assertContains(response, review.review_rate)
        self.assertContains(response, review2.review_title)
        self.assertContains(response, review2.review_description)
        self.assertContains(response, review2.review_rate)
