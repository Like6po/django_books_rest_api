import pytest
from django.urls import reverse
from rest_framework import status

from api.v1.models.confirm_code import ConfirmCode
from tests.base import RegisterFunc
from tests.consts import TEST_EMAIL


@pytest.mark.django_db
class TestConfirmView(RegisterFunc):

    def test_invalid(self, client):
        self.register(client)
        response = client.get(reverse("confirm", kwargs={"code": "123"}))
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data.get("status") == "Failed"
        assert data.get("detail") == "Link not valid"

    def test_valid(self, client):
        self.register(client)
        confirm_code = ConfirmCode.objects.get(user__email=TEST_EMAIL)
        response = client.get(reverse("confirm", kwargs={"code": confirm_code.id}))
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data.get('status') == 'Success'
        assert data.get('detail') == 'Account activated'
