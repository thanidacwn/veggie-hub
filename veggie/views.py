from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, State, Restaurant
from .forms import ReviewForm
import pandas as pd
import ssl


def get_data(request):
    """Get data from csv file and save to database."""
    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_csv('https://raw.githubusercontent.com/thanidacwn/veggie-data/master/last_data.csv')
    for index, row in df.iterrows():
        all_category = row["category"].split(", ")
        for _ in all_category:
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
    return HttpResponse("Hello, veggie!")


def index(request):
    """Display all restaurants."""
    all_restaurants = Restaurant.objects.all()
    context = {
        "all_restaurants": all_restaurants,
    }
    return render(request, "veggie/home.html", context)


@login_required
def add_review(request: HttpRequest, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == "POST":
        formset = ReviewForm(request.POST, instance=restaurant)
        if formset.is_valid():
            formset.save()
            restaurant.save()
            return redirect("veggie:detail")
    else:
        formset = ReviewForm(initial={'restaurant': restaurant_id,})
        context = {
            'restaurant': restaurant,
            'formset': formset,
        }
    return render(request, 'veggie/add_review.html', context)
