from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Category model"""
    category_text = models.CharField(verbose_name="category_text", max_length=255)

    def get_restaurants(self):
        """Return all restaurants in this category."""
        return self.restaurant_set.all()

    def __str__(self):
        return self.category_text


class State(models.Model):
    """State model"""
    state_text = models.CharField(verbose_name="state_text", max_length=255)

    def get_restaurants(self):
        """Return all restaurants in this state."""
        return self.restaurant_set.all()

    def __str__(self):
        return self.state_text


class Restaurant(models.Model):
    """Restaurant model"""
    restaurant_text = models.CharField(verbose_name="restaurant_text", max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.CharField(verbose_name="city", max_length=255)
    location = models.CharField(verbose_name="location", max_length=255)
    restaurant_link = models.CharField(verbose_name="restaurant_link", max_length=255)
    menu_link = models.CharField(verbose_name="menu_link", max_length=255)
    price_rate = models.CharField(verbose_name="price_rate", max_length=255)

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
        return total_rate / self.get_reviews_amount

    @property
    def get_reviews_amount(self):
        """Return the amount of reviews for this restaurant."""
        return self.review_set.count()

    def __str__(self):
        return self.restaurant_text


class Review(models.Model):
    """Review model"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_title = models.CharField(verbose_name="review_title", max_length=255)
    review_description = models.CharField(verbose_name="review_description", max_length=255)
    review_rate = models.IntegerField(verbose_name="review_rate", default=0)
    price_rate = models.CharField(verbose_name="price_rate", max_length=50)
    review_date = models.DateTimeField(verbose_name="review_date", auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.restaurant.restaurant_text} by {self.review_user.username}"
