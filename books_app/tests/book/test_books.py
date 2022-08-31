import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import BaseClientMixin, UnauthorizedTestMixin


@pytest.mark.django_db
class TestBooksGetView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books')

    def test_valid(self, fixture_users_repository):
        response = self.client.get(path=self.url,
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestBooksPostView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books')

    valid_request = {
        "name": "some book test",
        "publish_date": "2020-11-11",
        "category": 1
    }

    invalid_requests = [
        {},
        {"bla": 'bla'},
        {"name": "some book test",
         "publish_date": "fdsfffds",
         "category": 1}
    ]

    def test_with_admin_or_author_role(self, fixture_users_repository):
        for user in [fixture_users_repository.author, fixture_users_repository.admin]:
            response = self.client.post(path=self.url,
                                        data=self.valid_request,
                                        Authorization=user)
            assert response.status_code == status.HTTP_201_CREATED

    def test_with_user_role(self, fixture_users_repository):
        response = self.client.post(path=self.url,
                                    data=self.valid_request,
                                    Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_invalid(self, fixture_users_repository):
        for request in self.invalid_requests:
            response = self.client.post(path=self.url,
                                        data=request,
                                        Authorization=fixture_users_repository.author)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
