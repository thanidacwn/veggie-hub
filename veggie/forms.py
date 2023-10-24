from .models import *
from django.forms import ModelForm, Textarea


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["restaurant", "review_user", "review_title",
                "review_description", "review_rate", "review_date"]

        widgets = {
            "review_title": Textarea(attrs={'cols': 80, 'row': 8}),
            'review_description': Textarea(attrs={'cols': 80, 'rows': 8}),
        }
