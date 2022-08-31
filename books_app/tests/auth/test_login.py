import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import BaseClientMixin
from tests.consts import TEST_PASSWORD


@pytest.mark.django_db
class TestLoginView(BaseClientMixin):
    url = reverse('login')

    invalid_request = [
        {
            "email": "",
            "password": "admin"
        },
        {
            "email": "someinvalid@mail.ru"
        }
    ]

    def test_valid(self, fixture_users_repository):
        for user in [fixture_users_repository.user, fixture_users_repository.author, fixture_users_repository.admin]:
            response = self.client.post(path=self.url,
                                        data={"email": user.email,
                                              "password": TEST_PASSWORD})
            assert response.status_code == status.HTTP_200_OK

    def test_invalid(self, fixture_users_repository):
        for request in self.invalid_request:
            response = self.client.post(path=self.url,
                                        data=request)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
