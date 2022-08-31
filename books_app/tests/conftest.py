from dataclasses import dataclass

import pytest
from django.core.management import call_command

from api.v1.models.user import User


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "test_fixture.json")


@pytest.fixture
def fixture_users_repository():
    @dataclass
    class FixtureUsersRepository:
        user: User
        author: User
        admin: User

    return FixtureUsersRepository(
        user=User.objects.filter(role=0).first(),
        author=User.objects.filter(role=1).first(),
        admin=User.objects.filter(role=2).first()
    )
