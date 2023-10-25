from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from .models import Category, State, Restaurant
import pandas as pd
import ssl


def index(request):
    """Display all restaurants."""
    all_restaurants = Restaurant.objects.all()
    context = {
        "all_restaurants": all_restaurants,
    }
    return render(request, "veggie/home.html", context)


def home(request):
    """Get data from csv file and save to database."""
    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_csv('https://raw.githubusercontent.com/thanidacwn/veggie-data/master/last_data.csv')
    for index, row in df.iterrows():
        all_category = row["category"].split(", ")
        for cate in all_category:
            category = Category.objects.get_or_create(category_text=row["category"])[0]
            state = State.objects.get_or_create(state_text=row["state"])[0]
            restaurant = Restaurant(restaurant_text=row["restaurant_text"],
                        category=category,
                        state=state, city=row["city"],
                        location=row["location"],
                        restaurant_link=row["restaurant_link"],
                        menu_link=row["menu_link"],
                        price_rate=row["price_rate"],
                        image=row["image"])
            restaurant.save()
    return HttpResponse("Hello, world. You're at the home page.")


class DetailView(generic.DetailView):
    """Detail view page of this application."""
    model = Restaurant
    template_name = 'veggie/detail.html'

    def get(self, request, *args, **kwargs):
        """Redirect user to corresponding pages"""
        try:
            restaurant = get_object_or_404(Restaurant, pk=kwargs["pk"])
        except (KeyError, Restaurant.DoesNotExist):
            messages.error(request, 'Requested restaurant does not exist')
            return HttpResponseRedirect(reverse('veggie:index'))
        return render(request, 'veggie/detail.html', {
            'restaurant': restaurant})
