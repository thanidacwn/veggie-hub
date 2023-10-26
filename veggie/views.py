from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Category, State, Restaurant
import pandas as pd
import ssl


def filtered_categories() -> list:
    all_categories = ["All"]
    for category in Category.objects.all():
        # print([category.strip() for category in category.category_text.split(', ')]) 
        for cat in [category.strip() for category in category.category_text.split(', ')]:
            if cat not in all_categories:
                all_categories.append(cat)
    print(all_categories)
    return all_categories


def filtered_states() -> list:
    all_states = ['All']
    for state in State.objects.all():
        if state not in all_states:
            all_states.append(state)
    print(all_states) # print to check state
    return all_states


class RestaurantsView(generic.ListView):
    template_name = 'veggie/home.html'
    
    def get(self, request):
        return render(request, 'veggie/home.html', 
            {
                'all_restaurants': Restaurant.objects.all(), 
                'all_categories': filtered_categories(),
                'all_states': filtered_states()
            }
        )


class GetRestaurantByCategory(generic.ListView):
    model = Restaurant
    template_name = 'veggie/home.html'

    def get(self, request, category_name):
        if category_name == 'All':
            return HttpResponseRedirect(reverse('veggie:index'))
        all_restaurants = Restaurant.objects.filter(category__category_text__icontains=category_name)
        print(all_restaurants)
        return render(request, 'veggie/home.html', 
            {
                'all_restaurants': all_restaurants,
                'all_categories': filtered_categories(),
                'all_states': filtered_states()
            }
        )


class GetRestaurantByState(generic.ListView):
    model = Restaurant
    template_name = 'veggie/home.html'

    def get(self, request, state_name):
        if state_name == "All":
            return HttpResponseRedirect(reverse('veggie:index'))
        all_restaurants = Restaurant.objects.filter(state__state_text__icontains=state_name)
        print(all_restaurants)
        return render(request, 'veggie/home.html', 
            {
                'all_restaurants': all_restaurants,
                'all_categories': filtered_categories(),
                'all_states': filtered_states()
            }
        )


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
