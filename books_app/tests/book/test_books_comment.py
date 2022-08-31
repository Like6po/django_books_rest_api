import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import BaseClientMixin, UnauthorizedTestMixin


@pytest.mark.django_db
class TestBooksCommentGetView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books_comments_detail', kwargs={"book_id": 1, "comment_id": 1})

    def test_get_exists_comment(self, fixture_users_repository):
        response = self.client.get(path=self.url,
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_200_OK

    def test_get_not_exists_book(self, fixture_users_repository):
        response = self.client.get(path=reverse("books_comments_detail", kwargs={"book_id": 0, "comment_id": 1}),
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_not_exists_comment(self, fixture_users_repository):
        response = self.client.get(path=reverse("books_comments_detail", kwargs={"book_id": 1, "comment_id": 0}),
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBooksCommentDeleteView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books_comments_detail', kwargs={"book_id": 1, "comment_id": 1})

    def test_delete_comment_by_user(self, fixture_users_repository):
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_comment_by_author(self, fixture_users_repository):
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.author)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.author)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_comment_by_admin(self, fixture_users_repository):
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = self.client.delete(path=self.url,
                                      Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_not_exists_book(self, fixture_users_repository):
        response = self.client.delete(path=reverse('books_comments_detail',
                                                   kwargs={"book_id": 0, "comment_id": 1}),
                                      Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_not_exists_comment(self, fixture_users_repository):
        response = self.client.delete(path=reverse('books_comments_detail',
                                                   kwargs={"book_id": 1, "comment_id": 0}),
                                      Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBookCommentUpdateView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('books_comments_detail', kwargs={"book_id": 1, "comment_id": 1})

    valid_request = {
        "text": "bla-bla"
    }

    invalid_requests = [
        {},
        {"bla": 'bla'}
    ]

    def test_edit_comment_by_user(self, fixture_users_repository):
        response = self.client.put(path=self.url,
                                   data=self.valid_request,
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_200_OK

    def test_edit_comment_by_author(self, fixture_users_repository):
        response = self.client.put(path=self.url,
                                   data=self.valid_request,
                                   Authorization=fixture_users_repository.author)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_edit_comment_by_admin(self, fixture_users_repository):
        response = self.client.put(path=self.url,
                                   data=self.valid_request,
                                   Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_200_OK

    def test_invalid(self, fixture_users_repository):
        for request in self.invalid_requests:
            response = self.client.put(path=self.url,
                                       data=request,
                                       Authorization=fixture_users_repository.admin)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
