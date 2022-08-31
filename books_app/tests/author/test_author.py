import pytest
from django.urls import reverse
from rest_framework import status

from tests.base import UnauthorizedTestMixin, BaseClientMixin


@pytest.mark.django_db
class TestAuthorGetView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('authors_detail', kwargs={"author_id": 1})

    invalid_kwargs = [
        {"author_id": 999999999999},
        {"author_id": 0}
    ]

    def test_author_get_exists_author(self, fixture_users_repository):
        response = self.client.get(path=reverse(viewname='authors_detail',
                                                kwargs={"author_id": fixture_users_repository.author.id}),
                                   Authorization=fixture_users_repository.user)
        assert response.status_code == status.HTTP_200_OK

    def test_get_not_exists_authors(self, fixture_users_repository):
        for kwargs in self.invalid_kwargs:
            response = self.client.get(path=reverse(viewname='authors_detail',
                                                    kwargs=kwargs),
                                       Authorization=fixture_users_repository.user)
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_try_get_user(self, fixture_users_repository):
        response = self.client.get(path=reverse(viewname='authors_detail',
                                                kwargs={"author_id": fixture_users_repository.user.id}),
                                   Authorization=fixture_users_repository.author)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAuthorDeleteView(BaseClientMixin, UnauthorizedTestMixin):
    url = reverse('authors_detail', kwargs={"author_id": 1})

    invalid_kwargs = [
        {"author_id": 999999999999},
        {"author_id": 0}
    ]

    def test_delete_self(self, fixture_users_repository):
        response = self.client.delete(path=reverse(viewname='authors_detail',
                                                   kwargs={"author_id": fixture_users_repository.admin.id}),
                                      Authorization=fixture_users_repository.admin)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_not_exist_users(self, fixture_users_repository):
        for kwargs in self.invalid_kwargs:
            response = self.client.delete(path=reverse(viewname='authors_detail', kwargs=kwargs),
                                          Authorization=fixture_users_repository.admin)
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_without_admin_role(self, fixture_users_repository):
        for authorization in [fixture_users_repository.user, fixture_users_repository.admin]:
            response = self.client.delete(path=reverse(viewname='authors_detail',
                                                       kwargs={"author_id": fixture_users_repository.admin.id}),
                                          Authorization=authorization)
            assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestAuthorUpdateView(BaseClientMixin, UnauthorizedTestMixin):
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

    def test_update_self(self, fixture_users_repository):
        for request in self.valid_requests:
            response = self.client.put(path=reverse(viewname='authors_detail',
                                                    kwargs={"author_id": fixture_users_repository.author.id}),
                                       data=request,
                                       Authorization=fixture_users_repository.author)
            data = response.json()
            assert response.status_code == status.HTTP_200_OK
            assert data.get('status') == 'Success'
            for key, value in request.items():
                assert data.get('detail').get(key) == value

    def test_update_not_exist_users(self, fixture_users_repository):
        for kwargs in self.invalid_kwargs:
            response = self.client.put(path=reverse(viewname='authors_detail', kwargs=kwargs),
                                       data={},
                                       Authorization=fixture_users_repository.admin)
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_another_users_without_admin_role(self, fixture_users_repository):
        for authorization in [fixture_users_repository.user, fixture_users_repository.author]:
            response = self.client.put(path=reverse(viewname='authors_detail',
                                                    kwargs=self.invalid_kwargs[0]),
                                       data={},
                                       Authorization=authorization)
            assert response.status_code == status.HTTP_403_FORBIDDEN
