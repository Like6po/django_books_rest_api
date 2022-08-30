import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import RegisterFunc
from tests.consts import TEST_EMAIL, TEST_PASSWORD


@pytest.mark.django_db
class TestLoginView(RegisterFunc):
    url = reverse('login')

    valid_request = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }

    invalid_request = [
        {
            "email": "",
            "password": "admin"
        },
        {
            "email": TEST_EMAIL
        }
    ]

    def test_valid(self, client):
        self.register(client)
        response = client.post(self.url, self.valid_request)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data.get('status') == 'Success'
        assert data.get('detail').get('access_token')
        assert data.get('detail').get('refresh_token')

    def test_invalid(self, client):
        self.register(client)
        for request in self.invalid_request:
            response = client.post(self.url, request)
            data = response.json()
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert data.get('status') == 'Failed'
