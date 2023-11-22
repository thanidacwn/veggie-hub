from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """
    Represents a category.

    Args:
        category_text (str): The text of the category.

    Methods:
        get_restaurants(): Return all restaurants in this category.

    Attributes:
        category_text (str): The text of the category.

    Returns:
        str: The text of the category.
    """
    category_text = models.CharField(verbose_name="category_text",
                                     max_length=255, null=True, blank=True)

    def get_restaurants(self):
        """Return all restaurants in this category."""
        return self.restaurant_set.all()

    def __str__(self):
        return self.category_text


class State(models.Model):
    """
    Represents a state.

    Args:
        state_text (str): The text of the state.

    Methods:
        get_restaurants(): Return all restaurants in this state.

    Attributes:
        state_text (str): The text of the state.

    Returns:
        str: The text of the state.
    """
    state_text = models.CharField(verbose_name="state_text", max_length=255)

    def get_restaurants(self):
        """Return all restaurants in this state."""
        return self.restaurant_set.all()

    def __str__(self):
        return self.state_text


class Restaurant(models.Model):
    """
    Represents a restaurant.

    Args:
        restaurant_text (str): The text of the restaurant.
        category (Category): The category of the restaurant.
        state (State): The state of the restaurant.
        city (str): The city of the restaurant.
        location (str): The location of the restaurant.
        restaurant_link (str): The link to the restaurant.
        menu_link (str): The link to the restaurant's menu.
        price_rate (str): The price rate of the restaurant.
        image (str): The URL of the restaurant's image.

    Properties:
        get_average_rate: Return the average rate for this restaurant.
        get_reviews_amount: Return the amount of reviews for this restaurant.

    Attributes:
        restaurant_text (str): The text of the restaurant.
        category (Category): The category of the restaurant.
        state (State): The state of the restaurant.
        city (str): The city of the restaurant.
        location (str): The location of the restaurant.
        restaurant_link (str): The link to the restaurant.
        menu_link (str): The link to the restaurant's menu.
        price_rate (str): The price rate of the restaurant.
        image (str): The URL of the restaurant's image.

    Returns:
        str: The text of the restaurant.
    """
    restaurant_text = models.CharField(verbose_name="restaurant_text",
                                       max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.CharField(verbose_name="city", max_length=255)
    location = models.CharField(verbose_name="location", max_length=255)
    restaurant_link = models.CharField(verbose_name="restaurant_link",
                                       max_length=255)
    menu_link = models.CharField(verbose_name="menu_link", max_length=255)
    price_rate = models.CharField(verbose_name="price_rate", max_length=255)
    image = models.URLField(verbose_name="image", max_length=255)

    @property
    def get_average_rate(self):
        """Return the average rate for this restaurant."""
        # if no review, return 0
        if self.get_reviews_amount == 0:
            return 0
        # get all reviews
        reviews = self.review_set.all()
        # calculate the average rate
        total_rate = 0
        for review in reviews:
            total_rate += review.review_rate
        return round(total_rate / self.get_reviews_amount, 2)

    @property
    def get_reviews_amount(self):
        """Return the amount of reviews for this restaurant."""
        return self.review_set.count()

    def __str__(self):
        return self.restaurant_text


class Review(models.Model):
    """
    Represents a review.

    Args:
        restaurant (Restaurant): The restaurant being reviewed.
        review_user (User): The user who wrote the review.
        review_title (str): The title of the review.
        review_description (str): The description of the review.
        review_rate (int): The rating given in the review.
        review_date (datetime): The date and time the review was created.

    Attributes:
        restaurant (Restaurant): The restaurant being reviewed.
        review_user (User): The user who wrote the review.
        review_title (str): The title of the review.
        review_description (str): The description of the review.
        review_rate (int): The rating given in the review.
        review_date (datetime): The date and time the review was created.

    Returns:
        str: The formatted string representation of the review.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_title = models.CharField(verbose_name="review_title",
                                    max_length=255)
    review_description = models.CharField(verbose_name="review_description",
                                          max_length=255)
    review_rate = models.IntegerField(verbose_name="review_rate", default=0)
    review_date = models.DateTimeField(verbose_name="review_date",
                                       default=timezone.now)

    def __str__(self):
        return f"{self.review_title} \
            {self.restaurant.restaurant_text} by {self.review_user.username}"


class BookMark(models.Model):
    """
    Represents a bookmark.

    Args:
        bookmark_user (User): The user who bookmarked the restaurant.
        restaurant (Restaurant): The restaurant being bookmarked.
        bookmark_date (datetime): The date and time the bookmark was created.

    Attributes:
        bookmark_user (User): The user who bookmarked the restaurant.
        restaurant (Restaurant): The restaurant being bookmarked.
        bookmark_date (datetime): The date and time the bookmark was created.

    Returns:
        str: The formatted string representation of the bookmark.
    """
    bookmark_user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    bookmark_date = models.DateTimeField(verbose_name="bookmark_date",
                                         default=timezone.now)

    def __str__(self):
        return f"{self.restaurant} saved by {self.bookmark_user}"
