import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import RegisterFunc


@pytest.mark.django_db
class TestRefreshView(RegisterFunc):
    url = reverse('refresh')

    invalid_requests = [
        {},
        {"bla": "bla"},
        {"refresh_token": "some_invalid_value"}
    ]

    def test_valid(self, client):
        register_data = self.register(client)
        response = client.post(self.url, {"refresh_token": register_data.get("detail").get("refresh_token")})
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data.get('status') == 'Success'
        assert data.get('detail').get('access_token')
        assert data.get('detail').get('refresh_token')

    def test_invalid(self, client):
        self.register(client)
        for request in self.invalid_requests:
            response = client.post(self.url, request)
            data = response.json()
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert data.get('status') == 'Failed'
