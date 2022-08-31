import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import UnauthorizedTestMixin, BaseClientMixin


@pytest.mark.django_db
class TestAuthorsGetView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('authors')

    def test_valid(self, fixture_users_repository):
        response = self.client.get(path=self.url,
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAuthorsPostView(BaseClientMixin, UnauthorizedTestMixin):
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

    def test_valid(self, fixture_users_repository):
        response = self.client.post(path=self.url,
                                    data=self.valid_request,
                                    Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_201_CREATED

        response = self.client.post(path=self.url,
                                    data=self.valid_request,
                                    Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_invalid_data(self, fixture_users_repository):
        for request in self.invalid_requests:
            response = self.client.post(path=self.url,
                                        data=request,
                                        Authorization=fixture_users_repository.admin)
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_without_admin_role(self, fixture_users_repository):

        for user in [fixture_users_repository.author, fixture_users_repository.user]:
            response = self.client.post(path=self.url,
                                        data=self.valid_request,
                                        Authorization=user)
            data = response.json()
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert data.get('detail') == 'Only admins can create authors'
