from rest_framework import status
from rest_framework.test import APIClient


class ParameterIsMissing(Exception):
    def __str__(self):
        return 'You must set Authorization parameter otherwise use use_auth=False'


def set_credentials(func):
    def wrapper(self, *args, **extra):
        if not extra.get('Authorization', None):
            return func(self, *args, **extra)

        user_fixture = extra.get('Authorization', None)
        self.credentials(HTTP_AUTHORIZATION='Bearer ' + user_fixture._generate_jwt_token())
        return func(self, *args, **extra)

    return wrapper


class BaseTestHttpClient(APIClient):
    @set_credentials
    def get(self, path, data=None, follow=False, **extra):
        return super(BaseTestHttpClient, self).get(path, data=None, follow=False, **extra)

    @set_credentials
    def post(self, path, data=None, format=None, content_type=None,
             follow=False, **extra):
        return super(BaseTestHttpClient, self).post(path, data=data, format=format, content_type=content_type,
                                                    follow=follow, **extra)

    @set_credentials
    def put(self, path, data=None, format=None, content_type=None,
            follow=False, **extra):
        return super(BaseTestHttpClient, self).put(path, data=data, format=format, content_type=content_type,
                                                   follow=follow, **extra)

    @set_credentials
    def patch(self, path, data=None, format=None, content_type=None,
              follow=False, **extra):
        return super(BaseTestHttpClient, self).patch(path, data=data, format=format, content_type=content_type,
                                                     follow=follow, **extra)

    @set_credentials
    def delete(self, path, data=None, format=None, content_type=None,
               follow=False, **extra):
        return super(BaseTestHttpClient, self).delete(path, data=data, format=format, content_type=content_type,
                                                      follow=follow, **extra)


class UnauthorizedTestMixin:
    url = None

    def test_unauthorized(self):
        client = APIClient()
        response = client.get(self.url)
        data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert data.get('detail') == 'Authentication credentials were not provided.'


class BaseClientMixin:
    client = BaseTestHttpClient()
