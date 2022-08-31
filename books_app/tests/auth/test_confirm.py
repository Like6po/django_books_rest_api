import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from api.v1.models.confirm_code import ConfirmCode
from tests.base import BaseClientMixin


@pytest.mark.django_db
class TestConfirmView(BaseClientMixin):

    def test_invalid(self):
        response = self.client.get(path=reverse("confirm", kwargs={"code": "123"}))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_valid(self, fixture_users_repository):
        confirm_code = ConfirmCode.objects.get(user=fixture_users_repository.user)
        confirm_code.created_at = datetime.datetime.now()
        confirm_code.save()
        response = self.client.get(path=reverse("confirm", kwargs={"code": confirm_code.id}))
        assert response.status_code == status.HTTP_200_OK
        assert ConfirmCode.objects.filter(user=fixture_users_repository.user).exists() is False

    def test_code_expired(self, fixture_users_repository):
        confirm_code = ConfirmCode.objects.get(user=fixture_users_repository.user)
        confirm_code.created_at = datetime.datetime.now() - datetime.timedelta(days=7)
        confirm_code.save()
        response = self.client.get(path=reverse("confirm", kwargs={"code": confirm_code.id}))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
