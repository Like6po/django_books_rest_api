import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.base import UnauthorizedTest, RegisterFunc, SetupUserFuncs


@pytest.mark.django_db
class TestAuthorsGetView(RegisterFunc, UnauthorizedTest, SetupUserFuncs):
    url = reverse('authors')

    def setup_user(self):
        self.init_user()
        self.user_set_active()

    def test_valid(self, client):
        data = self.register(client)
        self.setup_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {data.get('detail').get('access_token')}")
        response = client.get(self.url)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data.get('status') == 'Success'


@pytest.mark.django_db
class TestAuthorsPostView(UnauthorizedTest, RegisterFunc, SetupUserFuncs):
    url = reverse('authors')

    valid_request = {
        "first_name": "first_name",
        "second_name": "second_name",
        "email": "example@mail.ru"
    }

    invalid_requests = [
        {},
        {"bla": 'bla'},
        {"first_name": "first_name",
         "second_name": "second_name",
         "email": "wrong_email"},
        {"second_name": "second_name",
         "email": "example@mail.ru"}
    ]

    def setup_user(self):
        self.init_user()
        self.user_set_active()
        self.user_set_role_admin()

    def test_valid(self, client):
        data = self.register(client)
        self.setup_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {data.get('detail').get('access_token')}")
        response = client.post(self.url, self.valid_request)
        data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert data.get('status') == 'Success'
        assert isinstance(data.get('detail'), dict)

        response = client.post(self.url, self.valid_request)
        data = response.json()
        assert response.status_code == status.HTTP_409_CONFLICT
        assert data.get('status') == 'Failed'

    def test_invalid_data(self, client):
        data = self.register(client)
        self.setup_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {data.get('detail').get('access_token')}")
        for request in self.invalid_requests:
            response = client.post(self.url, request)
            data = response.json()
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert data.get('status') == 'Failed'

        self.user_set_role_author()
        response = client.post(self.url, self.valid_request)
        data = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert data.get('status') == 'Failed'
        assert data.get('detail') == 'Only admins can create authors'
