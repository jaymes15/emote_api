import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


def sample_user(
    username="test_user",
    password="testpassword",
    first_name="John",
    last_name="Doe",
):
    """Helper to create sample user"""
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
