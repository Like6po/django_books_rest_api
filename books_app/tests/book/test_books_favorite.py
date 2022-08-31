import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import BaseClientMixin, UnauthorizedTestMixin


@pytest.mark.django_db
class TestBooksFavoriteGetView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('favorites')

    def test_valid(self, fixture_users_repository):
        response = self.client.get(path=self.url,
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestBooksFavoritePostView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('favorites')

    valid_request = {
        "book": 1
    }

    invalid_requests = [
        {},
        {"bla": 'bla'},
        {"name": "some book test",
         "publish_date": "fdsfffds",
         "category": 1},
    ]

    def test_valid(self, fixture_users_repository):
        response = self.client.post(path=self.url,
                                    data=self.valid_request,
                                    Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_201_CREATED

    def test_invalid(self, fixture_users_repository):
        for request in self.invalid_requests:
            response = self.client.post(path=self.url,
                                        data=request,
                                        Authorization=fixture_users_repository.user)
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_favorite_not_exits_book(self, fixture_users_repository):
        response = self.client.post(path=self.url,
                                    data={"book": 0},
                                    Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBooksFavoriteDeleteView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('favorites')

    valid_request = {
        "book": 1
    }

    invalid_requests = [
        {},
        {"bla": 'bla'},
        {"name": "some book test",
         "publish_date": "fdsfffds",
         "category": 1},
    ]

    def test_valid(self, fixture_users_repository):
        response = self.client.delete(path=self.url,
                                      data=self.valid_request,
                                      Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        self.client.post(path=self.url,
                         data=self.valid_request,
                         Authorization=fixture_users_repository.user)
        response = self.client.delete(path=self.url,
                                      data=self.valid_request,
                                      Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_invalid(self, fixture_users_repository):
        for request in self.invalid_requests:
            response = self.client.delete(path=self.url,
                                          data=request,
                                          Authorization=fixture_users_repository.user)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
