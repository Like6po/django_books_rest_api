import pytest
from django.urls import reverse
from rest_framework import status

from tests.consts import TEST_EMAIL, TEST_PASSWORD


@pytest.mark.django_db
class TestRegisterUserView:
    url = reverse('register_user')

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

    def test_valid(self, client):
        response = client.post(self.url, self.valid_request)
        data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert data.get('status') == 'Success'
        assert data.get('detail').get('access_token')
        assert data.get('detail').get('refresh_token')

    def test_invalid(self, client):
        for request in self.invalid_requests:
            response = client.post(self.url, request)
            data = response.json()
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert data.get('status') == 'Failed'


@pytest.mark.django_db
class TestRegisterAuthorView:
    url = reverse('register_author')

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
            "password": TEST_PASSWORD
        },

        {
            "email": TEST_EMAIL,
            "first_name": "first_name",
            "password": TEST_PASSWORD
        }
    ]

    def test_valid(self, client):
        response = client.post(self.url, self.valid_request)
        data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert data.get('status') == 'Success'
        assert data.get('detail').get('access_token')
        assert data.get('detail').get('refresh_token')

    def test_invalid(self, client):
        for request in self.invalid_requests:
            response = client.post(self.url, request)
            data = response.json()
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert data.get('status') == 'Failed'
