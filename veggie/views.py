from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseBadRequest
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
    """Returns
        assert  list: A list of filtered categories.
    """
    all_categories = ["All"]
    for category in Category.objects.all():
        # print([category.strip() for category in category.category_text.split(', ')]) 
        for cat in [category.strip() for category in category.category_text.split(', ')]:
            if cat not in all_categories:
                all_categories.append(cat)
    return all_categories


def filtered_states() -> list:
    """
    Returns a list of filtered states.

    Returns:
        list: A list of filtered states.
    """
    all_states = ['All']
    for state in State.objects.all():
        if state not in all_states:
            all_states.append(state.state_text)
    return all_states


class RestaurantsView(generic.ListView):
    """
    A view for rendering the restaurants page.

    This view extends the generic ListView provided by Django.
    It renders the 'veggie/home.html' template and passes the context data
    containing all restaurants, categories, and states to the template.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered HTTP response.
    """
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
    """
    A view for retrieving and rendering restaurants based on selected category and state.

    This view extends the generic ListView provided by Django.
    It retrieves the selected category and state from the request's GET parameters.
    It filters the restaurants based on the selected category and state, and renders the 'veggie/home.html' template
    with the filtered restaurants and other necessary context data.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered HTTP response.
    """
    model = Restaurant
    template_name = 'veggie/home.html'

    def get(self, request):
        """
        Handles the GET request for retrieving and rendering restaurants based on selected category and state.

        This method retrieves the selected category and state from the request's GET parameters.
        It filters the restaurants based on the selected category and state.
        If there are no restaurants matching the selected category and state, it displays a message to the user.
        If both the category and state are set to "All", it redirects to the 'veggie:index' URL.
        Otherwise, it renders the 'veggie/home.html' template with the filtered restaurants and other necessary context data.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered HTTP response.
        """
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


def get_data(request):
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
    return HttpResponse("Hello, world. You got the data!")


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


@login_required
def delete_review(request: HttpRequest, pk):
    """
    Deletes a review for a restaurant.

    This view function is decorated with `@login_required` to ensure that only authenticated users can delete reviews.
    It retrieves the restaurant object based on the provided primary key.
    If the restaurant does not exist or the primary key is invalid, it returns a bad request response.
    It then attempts to retrieve the redirect URL for the user's reviews page.
    If the redirect URL cannot be obtained or the user's review for the restaurant does not exist, it returns a bad request response.
    If the user's review exists, it deletes the review and displays a success message.
    Finally, it redirects the user to the appropriate page.

    Args:
        request (HttpRequest): The HTTP request object.
        pk: The primary key of the restaurant.

    Returns:
        HttpResponse: The redirected HTTP response.
    """
    try:
        restaurant = Restaurant.objects.get(pk=pk)
    except (Restaurant.DoesNotExist, ValueError):
        return HttpResponseBadRequest(f"{pk} does not exist!")

    try:
        redirect_url = reverse('veggie:myreviews')
    except (Review.DoesNotExist, ValueError):
        redirect_url = request.META.get('HTTP_REFERER', reverse('veggie:index'))
        return HttpResponseBadRequest("Review does not exist.")

    user_review = Review.objects.get(restaurant=restaurant, review_user=request.user)
    if not vote:
        messages.error(request, "You did not review this restaurant yet!")
        return redirect(redirect_url)
    user_review.delete()
    messages.info(request, f"Your review at {restaurant.restaurant_text} has been deleted.")
    return redirect(redirect_url)
