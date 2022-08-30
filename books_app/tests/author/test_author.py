import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.base import UnauthorizedTest, RegisterFunc, SetupUserFuncs


@pytest.mark.django_db
class TestAuthorGetView(RegisterFunc, UnauthorizedTest, SetupUserFuncs):
    url = reverse('authors_detail', kwargs={"author_id": 1})

    invalid_kwargs = [
        {"author_id": 999999999999},
        {"author_id": 0}
    ]

    def user_setup(self):
        self.init_user()
        self.user_set_active()
        self.user_set_role_author()

    def test_valid(self, client):
        data = self.register(client)

        self.user_setup()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {data.get('detail').get('access_token')}")
        response = client.get(reverse('authors_detail', kwargs={"author_id": data.get('detail').get('id')}))
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data.get('status') == 'Success'

    def test_invalid(self, client):
        register_data = self.register(client)

        self.user_setup()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {register_data.get('detail').get('access_token')}")

        for kwargs in self.invalid_kwargs:
            response = client.get(reverse('authors_detail', kwargs=kwargs))
            data = response.json()
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert data.get('status') == 'Failed'
            assert data.get('detail') == 'Author not found'

        self.user_set_role_default()
        response = client.get(reverse('authors_detail', kwargs={"author_id": register_data.get('detail').get('id')}))
        data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert data.get('status') == 'Failed'
        assert data.get('detail') == 'Author not found'


@pytest.mark.django_db
class TestAuthorDeleteView(RegisterFunc, UnauthorizedTest, SetupUserFuncs):
    url = reverse('authors_detail', kwargs={"author_id": 1})

    invalid_kwargs = [
        {"author_id": 999999999999},
        {"author_id": 0}
    ]

    def setup_user(self):
        self.init_user()
        self.user_set_active()
        self.user_set_role_admin()

    def test_valid(self, client):
        register_data = self.register(client)

        self.setup_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {register_data.get('detail').get('access_token')}")

        response = client.delete(reverse('authors_detail',
                                         kwargs={"author_id": register_data.get('detail').get('id')}))
        data = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert data.get('status') == 'Failed'
        assert data.get('detail') == 'Cant delete self account'

    def test_invalid(self, client):
        register_data = self.register(client)
        self.setup_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {register_data.get('detail').get('access_token')}")

        for kwargs in self.invalid_kwargs:
            response = client.delete(reverse('authors_detail', kwargs=kwargs))
            data = response.json()
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert data.get('status') == 'Failed'
            assert data.get('detail') == 'Author not found'

        self.user_set_role_default()

        response = client.delete(reverse('authors_detail',
                                         kwargs={"author_id": register_data.get('detail').get('id')}))
        data = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert data.get('status') == 'Failed'
        assert data.get('detail') == 'Only admins can delete accounts'


@pytest.mark.django_db
class TestAuthorUpdateView(RegisterFunc, UnauthorizedTest, SetupUserFuncs):
    url = reverse('authors_detail', kwargs={"author_id": 1})

    valid_requests = [
        {
            "first_name": "123"
        },
        {
            "second_name": "123"
        },
        {
            "first_name": "321",
            "second_name": "321"
        },
        {
            'patronymic': "test"
        }
    ]

    invalid_kwargs = [
        {"author_id": 999999999999},
        {"author_id": 0}
    ]

    def setup_user(self):
        self.init_user()
        self.user_set_active()
        self.user_set_role_author()

    def test_valid(self, client):
        register_data = self.register(client)
        self.setup_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {register_data.get('detail').get('access_token')}")
        for request in self.valid_requests:
            response = client.put(reverse('authors_detail',
                                          kwargs={"author_id": register_data.get('detail').get('id')}),
                                  request)
            data = response.json()
            assert response.status_code == status.HTTP_200_OK
            assert data.get('status') == 'Success'
            for key, value in request.items():
                assert data.get('detail').get(key) == value

    def test_invalid(self, client):
        register_data = self.register(client)
        self.setup_user()
        self.user_set_role_admin()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {register_data.get('detail').get('access_token')}")

        for kwargs in self.invalid_kwargs:
            response = client.put(reverse('authors_detail', kwargs=kwargs),
                                  {})
            data = response.json()
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert data.get('status') == 'Failed'
            assert data.get('detail') == 'Author not found'

        self.user_set_role_default()
        response = client.put(reverse('authors_detail', kwargs=self.invalid_kwargs[0]),
                              {})
        data = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert data.get('status') == 'Failed'
        assert data.get('detail') == 'Only admins can change another accounts'
