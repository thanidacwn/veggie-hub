from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from .models import Category, State, Restaurant
from .forms import ReviewForm
import pandas as pd
import ssl


def filtered_categories() -> list:
    all_categories = ["All"]
    for category in Category.objects.all():
        # print([category.strip() for category in category.category_text.split(', ')]) 
        for cat in [category.strip() for category in category.category_text.split(', ')]:
            if cat not in all_categories:
                all_categories.append(cat)
    return all_categories


def filtered_states() -> list:
    all_states = ['All']
    for state in State.objects.all():
        if state not in all_states:
            all_states.append(state.state_text)
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


class GetRestaurantByCategoryAndState(generic.ListView):
    model = Restaurant
    template_name = 'veggie/home.html'

    def get(self, request):
        selected_category = request.GET.get('category')
        selected_state = request.GET.get('state')

        all_restaurants = Restaurant.objects.all()

        if selected_category != "All":
            all_restaurants = all_restaurants.filter(category__category_text__icontains=selected_category)
        
        if selected_state != "All":
            all_restaurants = all_restaurants.filter(state__state_text__icontains=selected_state)

        if not all_restaurants:
            messages.info(request, f'There are no restaurants in {selected_category} Category and {selected_state} State.')
        
        if selected_category == "All" and selected_state == "All":
            return HttpResponseRedirect(reverse('veggie:index'))

        return render(request, 'veggie/home.html', 
            {
                'all_restaurants': all_restaurants,
                'all_categories': filtered_categories(),
                'all_states': filtered_states(),
                'selected_category': selected_category,
                'selected_state': selected_state
            }
        )


def home(request):
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

        restaurant.save()
        return HttpResponse("Hello, veggie!")


@login_required
def add_review(request: HttpRequest, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == "POST":
        formset = ReviewForm(request.POST, instance=restaurant)
        if formset.is_valid():
            formset.save()
            messages.success(request, "review save!")
        else:
            # Form is not valid, display error messages
            messages.error(request, 'You did not review yet! Please add your review.')
        return HttpResponseRedirect(reverse("veggie:detail", kwargs={'pk': pk}))
    else:
        formset = ReviewForm(initial={'restaurant': pk,})
        context = {
            'restaurant': restaurant,
            'formset': formset,
        }
    return render(request, 'veggie/add_review.html', context)
