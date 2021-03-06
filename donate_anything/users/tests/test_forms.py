import pytest

from donate_anything.users.forms import UserCreationForm
from donate_anything.users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestUserCreationForm:
    def test_clean_username(self):
        # A user with proto_user params does not exist yet.
        proto_user = UserFactory.build()

        form = UserCreationForm(
            {
                "email": proto_user.email,
                "username": proto_user.username,
                "password1": proto_user._password,
                "password2": proto_user._password,
                "g-recaptcha-response": "PASSED",
                "terms": True,
            }
        )

        assert form.is_valid()
        assert form.clean_username() == proto_user.username

        # Creating a user.
        form.save()

        # The user with proto_user params already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                "email": proto_user.email,
                "username": proto_user.username,
                "password1": proto_user._password,
                "password2": proto_user._password,
                "g-recaptcha-response": "PASSED",
                "terms": True,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors

    def test_clean_terms(self):
        # A user with proto_user params does not exist yet.
        proto_user = UserFactory.build()

        form = UserCreationForm(
            {
                "email": proto_user.email,
                "username": proto_user.username,
                "password1": proto_user._password,
                "password2": proto_user._password,
                "g-recaptcha-response": "PASSED",
                "terms": False,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "terms" in form.errors

        form = UserCreationForm(
            {
                "email": proto_user.email,
                "username": proto_user.username,
                "password1": proto_user._password,
                "password2": proto_user._password,
                "g-recaptcha-response": "PASSED",
                "terms": True,
            }
        )

        assert form.is_valid()
