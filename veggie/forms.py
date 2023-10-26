from .models import *
from django.forms import ModelForm


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["restaurant", "review_user", "review_title",
                "review_description", "review_rate", "review_date"]
