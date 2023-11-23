"""Django app config for veggie app."""
from django.apps import AppConfig


class VeggieConfig(AppConfig):
    """
    Configuration class for the Veggie app.

    Attributes:
        default_auto_field (str): The default auto field for the app.
        name (str): The name of the app.

    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "veggie"

