from django.http import HttpResponse
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
                        price_rate=row["price_rate"])
        restaurant.save()
    return HttpResponse("Hello, world. You're at the home page.")