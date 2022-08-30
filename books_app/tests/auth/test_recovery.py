import pytest
from django.urls import reverse
from rest_framework import status

from api.v1.models.recovery_code import RecoveryCode
from tests.base import RegisterFunc
from tests.consts import TEST_EMAIL, TEST_PASSWORD


@pytest.mark.django_db
class TestRecoveryView(RegisterFunc):
    url = reverse("recovery")

    valid_request = {
        "email": TEST_EMAIL
    }

    invalid_requests = [
        {},
        {"email": "fdsfdsfdsf"},
        {"email": "wrong@mail.ru"},
        {"bla-bla": "bla-bla"}
    ]

    def test_invalid(self, client):
        self.register(client)
        for request in self.invalid_requests:
            response = client.post(self.url, request)
            data = response.json()
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert data.get("status") == "Failed"

    def test_valid(self, client):
        self.register(client)
        response = client.post(self.url, self.valid_request)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data.get('status') == 'Success'
        assert data.get('detail') == 'Waiting password'


@pytest.mark.django_db
class TestRecoveryCodeView(RegisterFunc):
    valid_request = {
        "password": TEST_PASSWORD
    }

    invalid_requests = [
        {},
        {"bla-bla": "bla-bla"},
        {"password": "123"}
    ]

    def request_recovery(self, client):
        client.post(reverse("recovery"), {"email": TEST_EMAIL})

    def test_valid(self, client):
        self.register(client)
        self.request_recovery(client)
        recovery_code = RecoveryCode.objects.get(user__email=TEST_EMAIL)
        response = client.post(reverse("recovery_code",
                                       kwargs={"code": recovery_code.id}), self.valid_request)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data.get("status") == "Success"
        assert data.get("detail") == "Password changed"

    def test_invalid(self, client):
        self.register(client)
        self.request_recovery(client)
        recovery_code = RecoveryCode.objects.get(user__email=TEST_EMAIL)
        for request in self.invalid_requests:
            response = client.post(reverse("recovery_code",
                                           kwargs={"code": recovery_code.id}), request)
            data = response.json()
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert data.get("status") == "Failed"

        response = client.post(reverse("recovery_code",
                                       kwargs={"code": "123"}), self.valid_request)
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data.get("status") == "Failed"
        assert data.get("detail") == "Link not valid"
