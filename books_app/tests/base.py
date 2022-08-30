from django.urls import reverse
from rest_framework import status

from api.v1.models.user import User
from tests.consts import TEST_EMAIL, TEST_PASSWORD


class UnauthorizedTest:
    url = None

    def test_unauthorized(self, client):
        response = client.get(self.url)
        data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert data.get('detail') == 'Authentication credentials were not provided.'


class RegisterFunc:
    def register(self, client):
        response = client.post(reverse('register_user'), {
            "email": TEST_EMAIL,
            "first_name": "first_name",
            "second_name": "second_name",
            "password": TEST_PASSWORD
        })
        return response.json()


class SetupUserFuncs:
    user = None

    def init_user(self):
        self.user = User.objects.get(email=TEST_EMAIL)

    def user_set_active(self):
        self.user.is_active = True
        self.user.save()

    def user_set_role_admin(self):
        self.user.role = 2
        self.user.save()

    def user_set_role_author(self):
        self.user.role = 1
        self.user.save()

    def user_set_role_default(self):
        self.user.role = 0
        self.user.save()
