import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from api.v1.models.recovery_code import RecoveryCode
from tests.base import BaseClientMixin
from tests.consts import TEST_PASSWORD


@pytest.mark.django_db
class TestRecoveryView(BaseClientMixin):
    url = reverse("recovery")

    invalid_requests = [
        {},
        {"email": "fdsfdsfdsf"},
        {"email": "wrong@mail.ru"},
        {"bla-bla": "bla-bla"}
    ]

    def test_invalid(self):
        for request in self.invalid_requests:
            response = self.client.post(path=self.url,
                                        data=request)
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_valid(self, fixture_users_repository):
        response = self.client.post(path=self.url,
                                    data={"email": fixture_users_repository.admin.email})
        assert response.status_code == status.HTTP_200_OK
        assert RecoveryCode.objects.filter(user=fixture_users_repository.admin).exists() is True


@pytest.mark.django_db
class TestRecoveryCodeView(BaseClientMixin):
    valid_request = {
        "password": TEST_PASSWORD
    }

    invalid_requests = [
        {},
        {"bla-bla": "bla-bla"},
        {"password": "123"}
    ]

    def test_valid(self, fixture_users_repository):
        recovery_code = RecoveryCode.objects.get(user=fixture_users_repository.user)
        recovery_code.created_at = datetime.datetime.now()
        recovery_code.save()
        response = self.client.post(path=reverse("recovery_code",
                                                 kwargs={"code": recovery_code.id}),
                                    data=self.valid_request)
        assert response.status_code == status.HTTP_200_OK
        assert RecoveryCode.objects.filter(user=fixture_users_repository.user).exists() is False

    def test_invalid_request(self, fixture_users_repository):
        recovery_code = RecoveryCode.objects.get(user=fixture_users_repository.user)
        for request in self.invalid_requests:
            response = self.client.post(path=reverse("recovery_code",
                                                     kwargs={"code": recovery_code.id}),
                                        data=request)
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_code(self, fixture_users_repository):
        response = self.client.post(reverse("recovery_code",
                                            kwargs={"code": "123"}), self.valid_request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_code_expired(self, fixture_users_repository):
        recovery_code = RecoveryCode.objects.get(user=fixture_users_repository.user)
        recovery_code.created_at = datetime.datetime.now() - datetime.timedelta(days=7)
        recovery_code.save()
        response = self.client.post(path=reverse("recovery_code",
                                                 kwargs={"code": recovery_code.id}),
                                    data=self.valid_request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
