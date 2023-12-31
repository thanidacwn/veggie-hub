""""Views for the veggie app."""
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpRequest, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from .models import Category, State, Restaurant, Review, BookMark
from .forms import ReviewForm
import pandas as pd
import ssl


def filtered_categories() -> list:
    """
    Return a list of filtered categories.

    Returns:
        list: A list of filtered categories.

    """
    all_categories = ["All"]
    for category in Category.objects.all():
        for cat in [category.strip() for category in
                    category.category_text.split(', ')]:
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
    A view for retrieving and rendering restaurants
    based on selected category and state.

    This view extends the generic ListView provided by Django.
    It retrieves the selected category and state from
    the request's GET parameters. It filters the restaurants
    based on the selected category and state,
    and renders the 'veggie/home.html' template
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
        Handles the GET request for retrieving and rendering
        restaurants based on selected category and state.

        This method retrieves the selected category and state
        from the request's GET parameters.
        It filters the restaurants based on the selected category and state.
        If there are no restaurants matching the selected category and state,
        it displays a message to the user. If both the category and
        state are set to "All", it redirects to the 'veggie:index' URL.
        Otherwise, it renders the 'veggie/home.html' template with the
        filtered restaurants and other necessary context data.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered HTTP response.
        """
        selected_category = request.GET.get('category')
        selected_state = request.GET.get('state')

        all_restaurants = Restaurant.objects.all()

        if selected_category != "All":
            all_restaurants = all_restaurants.filter(
                category__category_text__icontains=selected_category)

        if selected_state != "All":
            all_restaurants = all_restaurants.filter(
                state__state_text__icontains=selected_state)

        if not all_restaurants:
            messages.info(request,
                          f'There are no restaurants in\
                          {selected_category} Category and\
                          {selected_state} State.')

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
    """
    Fetch and save data from a remote CSV file to the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response indicating the success of the operation.

    """
    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_csv(
        'https://raw.githubusercontent.com/thanidacwn/veggie-data/master/test_data.csv')
    for index, row in df.iterrows():
        all_category = row["category"].split(", ")
        for cate in all_category:
            category = Category.objects.get_or_create(
                category_text=row["category"])[0]
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
    """
    A view for displaying the details of a restaurant.

    Attributes:
        model (Restaurant): The model associated with the view.
        template_name (str): The name of the template
        to be used for rendering the view.

    Methods:
        get: Handle GET requests for the view.

    """
    model = Restaurant
    template_name = 'veggie/detail.html'

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for the view.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response.

        """
        try:
            restaurant = get_object_or_404(Restaurant, pk=kwargs["pk"])
        except (KeyError, Http404, Restaurant.DoesNotExist):
            messages.error(request, 'Requested restaurant does not exist')
            return HttpResponseRedirect(reverse('veggie:index'))
        try:
            reviews = Review.objects.filter(restaurant=restaurant).order_by('-review_date')
        except Review.DoesNotExist:
            reviews = []
        return render(request, 'veggie/detail.html', {
            'restaurant': restaurant,
            'reviews': reviews,
            'bookmarks': BookMark.objects.filter(restaurant=restaurant).order_by('-bookmark_date')
        })


class MyReviews(generic.ListView):
    """
    A view for displaying the reviews of the current user.

    Attributes:
        template_name (str): The name of the template
        to be used for rendering the view.
        context_object_name (str): The name of the
        context variable containing the reviews.

    Methods:
        get_queryset: Return the queryset of reviews.

    """
    template_name = 'veggie/my_reviews.html'
    context_object_name = 'reviews_list'

    def get_queryset(self):
        """
        Return the queryset of reviews.

        Returns:
            QuerySet: The queryset of reviews.
        """
        return Review.objects.filter(
            review_user_id=self.request.user).order_by('-review_date')


@login_required
def add_review(request, pk):
    """
    Handle the addition of a review for a restaurant.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the restaurant.

    Returns:
        HttpResponse: The HTTP response.

    """
    restaurant = get_object_or_404(Restaurant, pk=pk)
    review = Review.objects.filter(restaurant=restaurant, review_user=request.user).first()

    if review:
        # User already has a review for this restaurant
        messages.error(request, 'You have already submitted a review for this restaurant.')
        return HttpResponseRedirect(reverse("veggie:detail", 
                                            kwargs={'pk': pk}))

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            # Create a new review instance,
            # set its fields, and save it
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.review_user = request.user
            review.save()

            messages.success(request, "Review saved!")
            return HttpResponseRedirect(reverse("veggie:detail",
                                                kwargs={'pk': pk}))
        else:
            messages.error(request, 'Review form is not valid.\
                           Please check your input.')
    else:
        form = ReviewForm()

    context = {'restaurant': restaurant, 'review': review, 'form': form}
    return render(request, 'veggie/add_review.html', context)


@login_required
def edit_review(request, pk):
    # restaurant = get_object_or_404(Restaurant, pk=pk)
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review.review_user = request.user
            review.review_rate = form.cleaned_data['review_rate']
            review.review_title = form.cleaned_data['review_title']
            review.review_description = form.cleaned_data['review_description']
            review.save()

            messages.success(request, "Review edited!")
            return HttpResponseRedirect(reverse("veggie:my_reviews",
                                    kwargs={'pk': review.restaurant.pk}))
        else:
            messages.error(request, 'Review form is not valid.\
                           Please check your input.')
    else:
        form = ReviewForm()

    context = {'restaurant': review.restaurant, 'review': review, 'form': form}
    return render(request, 'veggie/edit_review.html', context)


@login_required
def delete_review(request: HttpRequest, pk):
    """
    Deletes a review for a restaurant.

    This view function is decorated with `@login_required` to
    ensure that only authenticated users can delete reviews.
    It retrieves the restaurant object based on the provided primary key.
    If the restaurant does not exist or the primary key is invalid,
    it returns a bad request response.
    It then attempts to retrieve the redirect URL for the user's reviews page.
    If the redirect URL cannot be obtained or
    the user's review for the restaurant does not exist,
    it returns a bad request response.
    If the user's review exists,
    it deletes the review and displays a success message.
    Finally, it redirects the user to the appropriate page.

    Args:
        request (HttpRequest): The HTTP request object.
        pk: The primary key of the restaurant.

    Returns:
        HttpResponse: The redirected HTTP response.
    """
    try:
        redirect_url = reverse('veggie:my_reviews', kwargs={'pk': pk})
    except (Review.DoesNotExist, ValueError):
        redirect_url = request.META.get('HTTP_REFERER',
                                        reverse('veggie:index'))
        return HttpResponseBadRequest("Review does not exist.")

    user_review = Review.objects.filter(
        review_user=request.user, pk=pk)
    if not user_review:
        messages.error(request,
                       "You did not review this restaurant yet!")
        return redirect(redirect_url)
    user_review.delete()
    messages.info(request, "Your review has been deleted.")
    return redirect(redirect_url)


class MyBookMarks(generic.ListView):
    """
    A view for displaying the bookmarks of the current user.

    Attributes:
        template_name (str): The name of the template
        to be used for rendering the view.
        context_object_name (str): The name of the context
        variable containing the bookmarks.

    Methods:
        get_queryset: Return the queryset of bookmarks.

    """
    template_name = 'veggie/my_bookmarks.html'
    context_object_name = 'all_bookmarks'

    def get_queryset(self):
        """
        Return the queryset of bookmarks for the current user.

        Returns:
            QuerySet: The queryset of bookmarks.

        """
        return BookMark.objects.filter(
            bookmark_user_id=self.request.user).order_by('-bookmark_date')


@login_required
def add_bookmark(request: HttpRequest, pk):
    """
    Add a bookmark for a restaurant.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the restaurant.

    Returns:
        HttpResponseRedirect: The HTTP redirect response.

    """
    restaurant = get_object_or_404(Restaurant, pk=pk)

    this_user = request.user
    bookmark = BookMark.objects.create(
        bookmark_user=this_user, restaurant=restaurant)
    bookmark.save()
    return HttpResponseRedirect(reverse('veggie:detail',
                                        args=(restaurant.pk, )))


@login_required
def delete_bookmark(request: HttpRequest, pk):
    """
    Delete a bookmark for a restaurant.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the restaurant.

    Returns:
        HttpResponseRedirect: The HTTP redirect response.

    """
    restaurant = get_object_or_404(Restaurant, pk=pk)

    this_user = request.user
    try:
        bookmark = BookMark.objects.get(
            bookmark_user=this_user, restaurant=restaurant)
        bookmark.delete()
    except BookMark.DoesNotExist:
        messages.error(request,
                       'This restaurant is not in My Bookmarks')
    return HttpResponseRedirect(reverse('veggie:detail',
                                        args=(restaurant.pk, )))
