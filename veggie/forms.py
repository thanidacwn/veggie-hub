from .models import Review
from django.forms import ModelForm, Textarea


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["review_rate", "review_title", "review_description"]

        widgets = {
            "review_title": Textarea(attrs={'cols': 80, 'rows': 8}),
            "review_description": Textarea(attrs={'cols': 80, 'rows': 8}),
        }
