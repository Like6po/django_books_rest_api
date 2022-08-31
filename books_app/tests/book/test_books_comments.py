import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import BaseClientMixin, UnauthorizedTestMixin


@pytest.mark.django_db
class TestBooksCommentsGetView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books_comments', kwargs={"book_id": 1})

    def test_valid(self, fixture_users_repository):
        response = self.client.get(path=self.url,
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_200_OK

    def test_invalid_kwarg(self, fixture_users_repository):
        response = self.client.get(path=reverse('books_comments', kwargs={"book_id": 0}),
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBooksCommentsPostView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books_comments', kwargs={"book_id": 1})

    valid_request = {
        "text": "bla-bla"
    }

    invalid_requests = [
        {},
        {"bla": 'bla'}
    ]

    def test_valid(self, fixture_users_repository):
        response = self.client.post(path=self.url,
                                    data=self.valid_request,
                                    Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_201_CREATED

    def test_invalid_kwarg(self, fixture_users_repository):
        response = self.client.get(path=reverse('books_comments', kwargs={"book_id": 0}),
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid(self, fixture_users_repository):
        for request in self.invalid_requests:
            response = self.client.post(path=self.url,
                                        data=request,
                                        Authorization=fixture_users_repository.author)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
