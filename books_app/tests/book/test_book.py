import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import BaseClientMixin, UnauthorizedTestMixin


@pytest.mark.django_db
class TestBookGetView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books_detail', kwargs={"book_id": 1})

    def test_get_exists_book(self, fixture_users_repository):
        response = self.client.get(path=self.url,
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_200_OK

    def test_get_not_exists_book(self, fixture_users_repository):
        response = self.client.get(path=reverse("books_detail", kwargs={"book_id": 0}),
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBookDeleteView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books_detail', kwargs={"book_id": 1})

    def test_delete_book_by_user(self, fixture_users_repository):
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_not_exists_book(self, fixture_users_repository):
        response = self.client.delete(path=reverse('books_detail', kwargs={"book_id": 0}),
                                      Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_book_by_author(self, fixture_users_repository):
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.author)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.author)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_book_by_admin(self, fixture_users_repository):
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBookUpdateView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books_detail', kwargs={"book_id": 1})

    valid_requests = [
        {"name": "new_name"},
        {"publish_date": "2019-01-01"},
        {"archived": True},
        {"category": 1}
    ]

    invalid_requests = [
        {"archived": "fds"}
    ]

    def test_edit_book_by_user(self, fixture_users_repository):
        response = self.client.put(path=self.url,
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_valid(self, fixture_users_repository):
        for request in self.valid_requests:
            response = self.client.put(path=self.url,
                                       data=request,
                                       Authorization=fixture_users_repository.admin)
            assert response.status_code == status.HTTP_200_OK

    def test_invalid(self, fixture_users_repository):
        for request in self.invalid_requests:
            response = self.client.put(path=self.url,
                                       data=request,
                                       Authorization=fixture_users_repository.admin)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
