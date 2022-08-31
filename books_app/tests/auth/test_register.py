import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import BaseClientMixin
from tests.consts import TEST_EMAIL, TEST_PASSWORD


class BaseRegisterView(BaseClientMixin):
    url = None

    valid_request = {
        "email": TEST_EMAIL,
        "first_name": "first_name",
        "second_name": "second_name",
        "password": TEST_PASSWORD
    }

    invalid_requests = [
        {},
        {
            "email": TEST_EMAIL,
            "first_name": "first_name",
            "second_name": "second_name",
            "password": "123"
        },
        {
            "email": "testru",
            "first_name": "first_name",
            "second_name": "second_name",
            "password": "123456"
        },

        {
            "email": "test111@mail.ru",
            "first_name": "first_name",
            "password": TEST_PASSWORD
        }
    ]

    def test_valid(self):
        response = self.client.post(path=self.url,
                                    data=self.valid_request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_invalid(self):
        for request in self.invalid_requests:
            response = self.client.post(path=self.url,
                                        data=request)
            assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRegisterAuthorView(BaseRegisterView):
    url = reverse('register_author')


@pytest.mark.django_db
class TestRegisterUserView(BaseRegisterView):
    url = reverse('register_user')
