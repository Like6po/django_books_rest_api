import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import BaseClientMixin


@pytest.mark.django_db
class TestRefreshView(BaseClientMixin):
    url = reverse('refresh')

    invalid_requests = [
        {},
        {"bla": "bla"},
        {"refresh_token": "some_invalid_value"}
    ]

    def test_valid(self, fixture_users_repository):
        r = fixture_users_repository.user._generate_refresh_jwt_token()
        response = self.client.post(path=self.url,
                                    data={"refresh_token": r})
        assert response.status_code == status.HTTP_200_OK

    def test_invalid(self, fixture_users_repository):
        for request in self.invalid_requests:
            response = self.client.post(path=self.url,
                                        data=request)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
