"""Forms for the veggie app."""
from .models import Review
from django.forms import ModelForm, Textarea


class ReviewForm(ModelForm):
    """
    A form for creating or updating a review.

    Attributes:
        Meta: Metadata options for the form.

    """
    class Meta:
        """
        Metadata options for the ReviewForm.

        Attributes:
            model (Review): The model associated with the form.
            fields (list): The fields to include in the form.
            widgets (dict): The widgets to use for specific fields.

        """
        model = Review
        fields = ["review_rate", "review_title", "review_description"]

        widgets = {
            "review_title": Textarea(attrs={'cols': 80, 'rows': 8}),
            "review_description": Textarea(attrs={'cols': 80, 'rows': 8}),
        }
